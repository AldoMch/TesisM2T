from __future__ import annotations
import re
import csv
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class ParsedDiagram:
    nodes: List[str] = field(default_factory=list)
    leaf_nodes: List[str] = field(default_factory=list)
    edges: List[Tuple[str, str]] = field(default_factory=list)
    node_types: Dict[str, str] = field(default_factory=dict)
    aliases: Dict[str, str] = field(default_factory=dict)
    entity_nodes: List[str] = field(default_factory=list)
    grouping_nodes: List[str] = field(default_factory=list)
    undirected_edges: List[Tuple[str, str]] = field(default_factory=list)
    duplicate_edge_count: int = 0
    layout_edge_count: int = 0
    parse_errors: List[str] = field(default_factory=list)


class PlantUMLParser:
    """Conservative component graph extraction; arrowheads alone give direction.

    Package/folder/frame declarations are grouping containers; other supported
    declarations are entities, including explicitly declared composite entities.
    Parallel relations collapse to ordered endpoint pairs. Unoriented links and
    layout links are reported separately. Unsupported structure fails validation.
    """

    GROUPING_TYPES = {"package", "folder", "frame"}
    _token = r'(?:"[^"\n]*"|\[[^\]\n]*\]|\([^()\n]*\)|[\w$](?:[\w$./-]*[\w$./])?)'
    _declaration = re.compile(
        r"^\s*(package|folder|frame|component|database|queue|cloud|node|rectangle|interface|actor|class|object|storage|artifact|file|agent|usecase|collections|card|hexagon|port|portin|portout)\s+"
        + rf"({_token})(?:\s*<<[^>]*>>)?(?:\s+as\s+({_token}))?",
        re.I,
    )
    _bracket = re.compile(
        r"^\s*\[([^\]]+)\](?:\s*<<[^>]*>>)?(?:\s+as\s+([\w$][\w$.-]*))?\s*(?:<<[^>]*>>)?\s*(?:#[\w]+)?\s*$"
    )
    _arrow = r"(?:<\|?|[}|*o+#x])?[-.=]+(?:\[[^\]\n]*\])?(?:(?:left|right|up|down|le|ri|do|[lrud])[-.=]*)?(?:\[[^\]\n]*\])?[-.=]*(?:[|]?>|[>{|*o+#x])?"
    _edge = re.compile(
        rf'^\s*({_token})\s*(?:"[^"]*"\s*)?({_arrow})\s*(?:"[^"]*"\s*)?({_token})(?:\s*(?::.*|#[\w]+))?\s*$',
        re.I,
    )

    def parse(self, puml_code: str) -> ParsedDiagram:
        nodes, aliases, parents = {}, {}, {}
        stack, raw_edges, errors = [], [], []
        block_stack, annotations = [], set()
        ignored_block, ignored_depth, layout_count = None, 0, 0

        def full_name(name, scope):
            return (
                f'{"::".join(scope) if scope else "Global"}::{self._clean_name(name)}'
            )

        def register(name, kind, alias, scope):
            canonical = full_name(name, scope)
            nodes[canonical], parents[canonical] = kind, tuple(scope)
            for key in (name, self._clean_name(name), alias):
                if key:
                    aliases[self._clean_name(key)] = canonical
            return canonical

        for lineno, raw_line in self._logical_lines(self._strip_comments(puml_code)):
            line = raw_line.strip()
            if not line or re.fullmatch(r"[-=]{2,}.*[-=]{2,}|[-=]{2,}", line):
                continue
            lower = line.lower()
            if ignored_block:
                if (
                    lower.startswith("end " + ignored_block)
                    or lower == "end" + ignored_block
                ) or (ignored_block == "style" and lower == "</style>"):
                    ignored_block = None
                continue
            if ignored_depth:
                ignored_depth += line.count("{") - line.count("}")
                continue
            if lower.startswith(("skinparam ", "<style>")):
                if lower.startswith("<style>"):
                    ignored_block = "style"
                else:
                    ignored_depth = max(0, line.count("{") - line.count("}"))
                continue
            if lower.startswith(("note ", "legend", "title ", "header", "footer")):
                if lower.startswith("note "):
                    alias_match = re.search(r"\bas\s+(\w+)", line)
                    if alias_match:
                        annotations.add(alias_match.group(1))
                if (
                    ":" not in line
                    and not re.match(r'^note\s+"[^"]*"\s+as\s+', line, re.I)
                    and lower.split()[0] in {"note", "legend", "header", "footer"}
                ):
                    ignored_block = lower.split()[0]
                continue
            if lower.startswith(
                (
                    "hide ",
                    "show ",
                    "left to right",
                    "top to bottom",
                    "scale ",
                    "set ",
                    "!",
                    "@",
                )
            ):
                continue
            if lower == "together {":
                block_stack.append(False)
                continue
            if line == "}":
                if block_stack:
                    if block_stack.pop():
                        stack.pop()
                else:
                    errors.append(f"line {lineno}: unmatched closing group")
                continue
            if line == "{":
                errors.append(f"line {lineno}: detached opening group is unsupported")
                continue
            macro = re.fullmatch(r"(\w+)\((.*)\)\s*(\{)?", line)
            if macro:
                name, args, opening = macro.groups()
                try:
                    args = next(csv.reader([args], skipinitialspace=True))
                except csv.Error:
                    args = []
                if (
                    name
                    in {
                        "System_Boundary",
                        "Container_Boundary",
                        "Enterprise_Boundary",
                        "Boundary",
                    }
                    and len(args) >= 2
                ):
                    register(args[1], "package", args[0], stack)
                    if opening:
                        stack.append(args[1])
                        block_stack.append(True)
                    continue
                if (
                    re.fullmatch(
                        r"(?:Person|System|Container|Component)(?:Db|Queue)?(?:_Ext)?",
                        name,
                    )
                    and len(args) >= 2
                ):
                    kind = (
                        "database"
                        if "Db" in name
                        else ("queue" if "Queue" in name else "component")
                    )
                    register(args[1], kind, args[0], stack)
                    continue
                if (
                    re.fullmatch(
                        r"(?:Rel|BiRel)(?:_[UDLR]|_Up|_Down|_Left|_Right|_Back)?", name
                    )
                    and len(args) >= 2
                ):
                    arrow = (
                        "<-->"
                        if name.startswith("BiRel")
                        else ("<--" if name.endswith("_Back") else "-->")
                    )
                    raw_edges.append((args[0], arrow, args[1], tuple(stack)))
                    continue
            line = re.sub(r"(?<=[-.])\(\)", "", line)
            edge = self._edge.fullmatch(line)
            if edge:
                src, arrow, dst = edge.groups()
                if re.search(r"\b(hidden|invis(?:ible)?)\b", arrow, re.I):
                    layout_count += 1
                else:
                    raw_edges.append((src, arrow, dst, tuple(stack)))
                continue
            decl = self._declaration.match(line)
            if decl:
                kind, first, second = decl.groups()
                name, alias = (
                    (second, first)
                    if second and second.startswith(('"', "["))
                    else (first, second)
                )
                kind = kind.lower()
                register(name, kind, alias, stack)
                tail = line[decl.end() :].strip()
                if "{" in tail:
                    if "}" in tail:
                        if tail[tail.index("{") + 1 : tail.rindex("}")].strip():
                            errors.append(
                                f"line {lineno}: nonempty inline block is unsupported"
                            )
                    elif kind in {"class", "object"}:
                        ignored_depth = 1
                    else:
                        stack.append(self._clean_name(name))
                        block_stack.append(True)
                continue
            bracket = self._bracket.fullmatch(line)
            if bracket:
                name, alias = bracket.groups()
                register(name, "component", alias, stack)
                continue
            if lower.startswith("()"):
                interface = re.match(
                    r"^\(\)\s*" + f"({self._token})" + r"(?:\s+as\s+([\w.-]+))?", line
                )
                if interface:
                    register(interface.group(1), "interface", interface.group(2), stack)
                    continue
            if re.fullmatch(r'"[^"]*"', line):
                register(line, "implicit", None, stack)
                continue
            if re.match(r"^[+~#-]\s+", line):
                continue
            if any(
                token in line
                for token in (
                    "--",
                    "..",
                    "->",
                    "<-",
                    "[",
                    "component ",
                    "package ",
                    "rectangle ",
                )
            ):
                errors.append(
                    f"line {lineno}: unsupported structural statement: {line[:140]}"
                )

        # PlantUML implicitly closes open grouping blocks at @enduml.
        def endpoint(raw, scope):
            clean = self._clean_name(raw)
            local = full_name(clean, scope)
            if local in nodes:
                return local
            if clean in aliases:
                return aliases[clean]
            nodes[local], parents[local], aliases[clean] = "implicit", scope, local
            return local

        edges, undirected = [], []
        for src, arrow, dst, scope in raw_edges:
            if (
                self._clean_name(src) in annotations
                or self._clean_name(dst) in annotations
            ):
                layout_count += 1
                continue
            a, b = endpoint(src, scope), endpoint(dst, scope)
            plain = re.sub(r"\[[^\]]*\]", "", arrow)
            left, right = plain.startswith("<"), plain.endswith(">")
            if right:
                edges.append((a, b))
            if left:
                edges.append((b, a))
            if not left and not right:
                undirected.append(tuple(sorted((a, b))))
        all_nodes = sorted(nodes)
        groups = [n for n in all_nodes if nodes[n] in self.GROUPING_TYPES]
        entities = [n for n in all_nodes if nodes[n] not in self.GROUPING_TYPES]
        parent_paths = {p for p in parents.values() if p}
        leaves = [
            n
            for n in all_nodes
            if tuple(n.removeprefix("Global::").split("::")) not in parent_paths
        ]
        return ParsedDiagram(
            nodes=all_nodes,
            leaf_nodes=leaves,
            edges=sorted(set(edges)),
            node_types=nodes,
            aliases=aliases,
            entity_nodes=entities,
            grouping_nodes=groups,
            undirected_edges=sorted(set(undirected)),
            duplicate_edge_count=len(edges) - len(set(edges)),
            layout_edge_count=layout_count,
            parse_errors=errors,
        )

    @staticmethod
    def _logical_lines(code):
        # Multiline bracket/quoted labels are display text, not new statements.
        buffer, start = "", 0
        for i, line in enumerate(code.splitlines(), 1):
            if buffer:
                buffer += r"\n" + line.strip()
            else:
                buffer, start = line, i
            brackets = buffer.count("[") - buffer.count("]")
            quotes = len(re.findall(r'(?<!\\)"', buffer)) % 2
            # A declaration ending in '[' is a member/detail block, not a label.
            detail_block = bool(re.match(r"^\s*\w+\s+\w+\s*\[\s*$", buffer))
            if (brackets > 0 and not detail_block) or quotes:
                continue
            yield start, buffer
            buffer = ""
        if buffer:
            yield start, buffer

    @staticmethod
    def _strip_comments(code: str) -> str:
        code = re.sub(r"/'.*?'/", "", code, flags=re.S)
        result, quoted, brackets = [], False, 0
        for line in code.splitlines():
            kept = []
            for i, char in enumerate(line):
                escaped = i > 0 and line[i - 1] == chr(92)
                if char == '"' and not escaped:
                    quoted = not quoted
                if not quoted:
                    if char == "[":
                        brackets += 1
                    elif char == "]":
                        brackets = max(0, brackets - 1)
                    elif char == "'" and not brackets:
                        break
                kept.append(char)
            result.append("".join(kept))
        return "\n".join(result)

    @staticmethod
    def _clean_name(value: str) -> str:
        clean = value.strip()
        if len(clean) >= 2 and (
            (clean[0] == clean[-1] == '"')
            or (clean[0], clean[-1]) in {("[", "]"), ("(", ")")}
        ):
            clean = clean[1:-1]
        return clean.replace("\n", "\\n")

    @classmethod
    def _normalize_key(cls, value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", cls._clean_name(value).lower())

    @classmethod
    def semantic_key(cls, value: str) -> str:
        return "::".join(
            filter(None, (cls._normalize_key(p) for p in value.split("::")))
        )

    @classmethod
    def label_key(cls, value: str) -> str:
        return cls._normalize_key(value.split("::")[-1])
