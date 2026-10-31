param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [ValidateSet("E-R2A", "G-R2A")]
    [string]$Dataset = "E-R2A",
    [string]$InputDir = "",
    [string]$OutputRoot = "",
    [string[]]$Models = @(
        "claude-sonnet-4-6",
        "deepseek-v3.2",
        "deepseek-v4.1-flash",
        "gpt-5",
        "qwen3-coder-480b-a35b-instruct"
    ),
    [string]$ModelProviderPrefix = "openai",
    [string]$ApiBase = $env:OPENAI_BASE_URL,
    [string]$MiniExe = "",
    [string[]]$MiniConfig = @(),
    [double]$CostLimit = 1.0,
    [int]$StepLimit = 20,
    [int]$WallTimeLimitSec = 900,
    [int]$CommandTimeoutSec = 180,
    [double]$Temperature = 0.0,
    [string[]]$Sample = @(),
    [switch]$Force,
    [switch]$DryRun,
    [switch]$StopOnError,
    [switch]$NoApiBase
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-AbsolutePath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
}

function Convert-ToForwardSlashPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return $Path.Replace("\", "/")
}

function Convert-ToSafePathSegment {
    param([Parameter(Mandatory = $true)][string]$Value)
    $safe = $Value -replace '[<>:"/\\|?*\s]+', "_"
    $safe = $safe.Trim("._")
    if ([string]::IsNullOrWhiteSpace($safe)) {
        return "model"
    }
    return $safe
}

function Get-ModelCallName {
    param(
        [Parameter(Mandatory = $true)][string]$ModelLabel,
        [string]$ProviderPrefix
    )
    if ([string]::IsNullOrWhiteSpace($ProviderPrefix) -or $ModelLabel.Contains("/")) {
        return $ModelLabel
    }
    return "$ProviderPrefix/$ModelLabel"
}

function Resolve-MiniExecutable {
    param([string]$ExplicitMiniExe)

    if (-not [string]::IsNullOrWhiteSpace($ExplicitMiniExe)) {
        $resolved = Resolve-AbsolutePath $ExplicitMiniExe
        if (Test-Path -LiteralPath $resolved -PathType Leaf) {
            return $resolved
        }
        throw "Mini executable not found: $resolved"
    }

    if (-not [string]::IsNullOrWhiteSpace($env:CONDA_PREFIX)) {
        $condaMini = Join-Path $env:CONDA_PREFIX "Scripts\mini.exe"
        if (Test-Path -LiteralPath $condaMini -PathType Leaf) {
            return $condaMini
        }
    }

    $command = Get-Command mini -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    throw @"
Cannot find mini-swe-agent executable.
Activate the mini-swe conda environment first, or pass -MiniExe explicitly"
"@
}

function Test-PlantUmlFile {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $false
    }
    $content = Get-Content -Raw -LiteralPath $Path
    return ($content -match '(?is)^\s*@startuml\b') -and ($content -match '(?is)@enduml\s*$')
}

$RootPath = Resolve-AbsolutePath $Root
$DatasetInputRoot = if ([string]::IsNullOrWhiteSpace($InputDir)) {
    Join-Path $RootPath "Dataset\$Dataset"
}
else {
    Resolve-AbsolutePath $InputDir
}

$ResolvedOutputRoot = if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    Join-Path $RootPath "runs\$Dataset\mini-swe-agent"
}
else {
    Resolve-AbsolutePath $OutputRoot
}

$MiniConfigSpecs = if ($MiniConfig.Count -gt 0) {
    $MiniConfig
}
else {
    @("mini.yaml", (Join-Path $PSScriptRoot "mini_c_r2a.yaml"))
}

if (-not (Test-Path -LiteralPath $DatasetInputRoot -PathType Container)) {
    throw "Input directory not found: $DatasetInputRoot"
}

$miniCommandPath = ""
if (-not $DryRun) {
    $miniCommandPath = Resolve-MiniExecutable $MiniExe
}

if (-not $DryRun -and $ModelProviderPrefix -eq "openai" -and [string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) {
    throw "OPENAI_API_KEY is not set. Set it in the current shell before running the baseline."
}

$allowedSamples = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($name in $Sample) {
    if (-not [string]::IsNullOrWhiteSpace($name)) {
        [void]$allowedSamples.Add($name)
    }
}

$samples = @(Get-ChildItem -LiteralPath $DatasetInputRoot -Recurse -Filter "checked_srs.md" -File |
    Sort-Object FullName |
    ForEach-Object {
        [pscustomobject]@{
            ProjectName = $_.Directory.Name
            SrsPath = $_.FullName
        }
    } |
    Where-Object {
        $allowedSamples.Count -eq 0 -or $allowedSamples.Contains($_.ProjectName)
    })

if (-not $samples -or $samples.Count -eq 0) {
    throw "No checked_srs.md files found under $DatasetInputRoot for the current selection."
}

$culture = [System.Globalization.CultureInfo]::InvariantCulture
$costLimitText = $CostLimit.ToString($culture)
$temperatureText = $Temperature.ToString($culture)
$failures = New-Object System.Collections.Generic.List[object]
$total = $Models.Count * $samples.Count
$index = 0
$failurePath = Join-Path $ResolvedOutputRoot "mini_swe_failures.csv"

if (-not $DryRun -and (Test-Path -LiteralPath $failurePath -PathType Leaf)) {
    Remove-Item -LiteralPath $failurePath
}

Write-Host "Root: $RootPath"
Write-Host "Dataset: $Dataset"
Write-Host "Input: $DatasetInputRoot"
Write-Host "Output: $ResolvedOutputRoot"
Write-Host "Models: $($Models -join ', ')"
Write-Host "Samples: $($samples.Count)"
Write-Host "Mini configs: $($MiniConfigSpecs -join ', ')"
Write-Host "Step limit: $StepLimit"
if (-not $NoApiBase -and -not [string]::IsNullOrWhiteSpace($ApiBase)) {
    Write-Host "API base: $ApiBase"
}

foreach ($modelLabel in $Models) {
    $modelDirName = Convert-ToSafePathSegment $modelLabel
    $modelCallName = Get-ModelCallName -ModelLabel $modelLabel -ProviderPrefix $ModelProviderPrefix

    foreach ($sampleInfo in $samples) {
        $index += 1
        $projectName = $sampleInfo.ProjectName
        $outputDir = Join-Path (Join-Path $ResolvedOutputRoot $modelDirName) $projectName
        $predictedPath = Join-Path $outputDir "predicted.puml"
        $trajectoryPath = Join-Path $outputDir "trajectory.traj.json"
        $taskPath = Join-Path $outputDir "task.txt"
        $metadataPath = Join-Path $outputDir "run_metadata.json"
        Write-Host "[$index/$total] $modelLabel :: $projectName"

        if ((Test-Path -LiteralPath $predictedPath -PathType Leaf) -and -not $Force) {
            Write-Host "  skipped: predicted.puml already exists"
            continue
        }

        $srsPromptPath = Convert-ToForwardSlashPath $sampleInfo.SrsPath
        $outputPromptPath = Convert-ToForwardSlashPath $predictedPath
        $outputPromptDir = Convert-ToForwardSlashPath $outputDir
        $stopExplorationStep = [Math]::Max(1, $StepLimit - 2)
        $writeFinalStep = [Math]::Max(1, $StepLimit - 1)

        $task = @"
R2A mini-swe-agent baseline task.

Dataset: $Dataset
Sample: $projectName
SRS path: $srsPromptPath
Output path: $outputPromptPath

Read the SRS file and generate a layered PlantUML component or deployment architecture diagram.

Write ONLY the final PlantUML source to:
$outputPromptPath

Rules:
- predicted.puml must begin with @startuml and end with @enduml.
- Do not use Markdown fences in predicted.puml.
- Do not add explanations to predicted.puml.
- Do not edit repository files except files under:
  $outputPromptDir
- Use architecture-level components, services, data stores, external systems, and major dependencies.
- Keep inferred components minimal and architecture-level rather than source-code class-level.
- Prefer Python or PowerShell commands for file IO because this run executes on Windows.
- Step budget policy: you have at most $StepLimit model calls. Stop exploration by model call $stopExplorationStep; write the best-effort final predicted.puml by model call $writeFinalStep; at model call $StepLimit, do not modify files further and submit.
- After verifying predicted.puml exists and contains valid PlantUML markers, finish by running exactly:
  echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT
"@

        if ($DryRun) {
            Write-Host "  dry-run: mini -m $modelCallName -> $predictedPath"
            continue
        }

        New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
        if (Test-Path -LiteralPath $predictedPath -PathType Leaf) {
            $backupPath = Join-Path $outputDir ("predicted.previous." + [guid]::NewGuid().ToString("N") + ".puml")
            Move-Item -LiteralPath $predictedPath -Destination $backupPath -ErrorAction Stop
            Write-Host "  previous prediction preserved: $backupPath"
        }
        Set-Content -LiteralPath $taskPath -Value $task -Encoding UTF8

        $metadata = [ordered]@{
            dataset = $Dataset
            project_name = $projectName
            model_label = $modelLabel
            model_call_name = $modelCallName
            provider_prefix = $ModelProviderPrefix
            api_base = if ($NoApiBase) { "" } else { $ApiBase }
            srs_path = $sampleInfo.SrsPath
            output_dir = $outputDir
            predicted_path = $predictedPath
            trajectory_path = $trajectoryPath
            task_path = $taskPath
            mini_config = $MiniConfigSpecs
            cost_limit = $CostLimit
            step_limit = $StepLimit
            wall_time_limit_sec = $WallTimeLimitSec
            command_timeout_sec = $CommandTimeoutSec
            temperature = $Temperature
        }
        $metadata | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $metadataPath -Encoding UTF8

        $miniArgs = @(
            "-m", $modelCallName,
            "--model-class", "litellm",
            "--agent-class", "default",
            "-l", $costLimitText,
            "-o", $trajectoryPath,
            "-t", $task
        )

        foreach ($configSpec in $MiniConfigSpecs) {
            $miniArgs += @("-c", $configSpec)
        }

        $miniArgs += @(
            "-c", "environment.cwd=$RootPath",
            "-c", "environment.timeout=$CommandTimeoutSec",
            "-c", "agent.step_limit=$StepLimit",
            "-c", "agent.wall_time_limit_seconds=$WallTimeLimitSec",
            "-c", "model.cost_tracking=ignore_errors",
            "-c", "model.model_kwargs.temperature=$temperatureText"
        )

        if (-not $NoApiBase -and -not [string]::IsNullOrWhiteSpace($ApiBase)) {
            $miniArgs += @("-c", "model.model_kwargs.api_base=$ApiBase")
        }

        try {
            $previousErrorActionPreference = $ErrorActionPreference
            $ErrorActionPreference = "Continue"
            try {
                & $miniCommandPath @miniArgs
                $exitCode = $LASTEXITCODE
            }
            finally {
                $ErrorActionPreference = $previousErrorActionPreference
            }
            if ($exitCode -ne 0) {
                throw "mini exited with code $exitCode"
            }
            if (-not (Test-PlantUmlFile $predictedPath)) {
                throw "predicted.puml is missing or does not contain @startuml/@enduml markers."
            }
            Write-Host "  generated: $predictedPath"
        }
        catch {
            $message = $_.Exception.Message
            Write-Host "  failed: $message" -ForegroundColor Red
            $failures.Add([pscustomobject]@{
                model = $modelLabel
                project_name = $projectName
                srs_path = $sampleInfo.SrsPath
                output_dir = $outputDir
                predicted_path = $predictedPath
                error = $message
            }) | Out-Null
            if ($StopOnError) {
                break
            }
        }
    }

    if ($StopOnError -and $failures.Count -gt 0) {
        break
    }
}

if ($failures.Count -gt 0) {
    New-Item -ItemType Directory -Force -Path $ResolvedOutputRoot | Out-Null
    $failures | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath $failurePath
    Write-Host "Completed with $($failures.Count) failure(s). See $failurePath" -ForegroundColor Red
    exit 1
}

Write-Host "Completed successfully."
