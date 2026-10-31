# Generation entry points

The released outputs are frozen. New runs should write to `runs/` and are not
expected to reproduce stochastic API responses byte-for-byte.

| Setting | Entry point | Runtime |
| --- | --- | --- |
| Direct LLM use | `direct.py` | Python, OpenAI-compatible endpoint |
| MetaGPT-based R2A workflow | `metagpt_r2a.py` | Python and MetaGPT |
| Mini-SWE-Agent | `mini_swe.ps1`, `mini_c_r2a.yaml` | PowerShell and the `mini` CLI |
| OpenHands | `openhands.sh` | Bash and the `openhands` CLI |

Inspect the supported options before starting a paid run:

```bash
python generation/direct.py --help
python generation/metagpt_r2a.py --help
```

Both Python entry points support `--dry-run`. The Mini-SWE launcher supports
`-DryRun`, and the OpenHands launcher supports `DRY_RUN=1`. These dry runs are
for inspecting input selection and task construction, not generation quality.
Use environment variables for credentials; no key is supplied by the release.

The MetaGPT pipeline uses analyst, architect, reviewer and refiner stages.
Configure its actual provider/model through MetaGPT's configuration.
`--model-label` labels output metadata and is not a provider-model override.

Mini-SWE and OpenHands launchers preserve the historical framework interfaces;
install framework versions compatible with those CLIs in separate environments.
Forced reruns preserve the previous prediction in a uniquely named backup and
require a newly written prediction before reporting success.
The pinned analysis requirements specify the offline analysis dependencies.

A different input, model/provider, budget, tool configuration or prompt
defines a new experimental run. Configure the provider endpoint explicitly;
no API endpoint or credential is bundled.
