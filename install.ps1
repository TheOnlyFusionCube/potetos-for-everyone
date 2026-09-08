$ErrorActionPreference = "Stop"

$Repository = if ($env:POTETOS_REPO) { $env:POTETOS_REPO } else { "TheOnlyFusionCube/potetos-for-everyone" }
$Ref = if ($env:POTETOS_REF) { $env:POTETOS_REF } else { "main" }
$Target = if ($env:POTETOS_TARGET) { $env:POTETOS_TARGET } else { (Get-Location).Path }
$Agent = if ($env:POTETOS_AGENT) { $env:POTETOS_AGENT } else { "all" }
$Action = if ($env:POTETOS_ACTION) { $env:POTETOS_ACTION } else { "auto" }
$Source = $env:POTETOS_SOURCE_DIR
$TempRoot = $null
$EphemeralSource = $false

function Find-Python {
    foreach ($candidate in @("python3", "python", "py")) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) { return $candidate }
    }
    throw "potetos: Python 3 is required."
}

try {
    if (-not $Source) {
        if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "bin/potetos"))) {
            $Source = $PSScriptRoot
        } else {
            $EphemeralSource = $true
            $TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("potetos-" + [guid]::NewGuid().ToString("N"))
            New-Item -ItemType Directory -Path $TempRoot | Out-Null
            $Archive = Join-Path $TempRoot "source.zip"
            $Extract = Join-Path $TempRoot "src"
            Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/$Repository/archive/$Ref.zip" -OutFile $Archive
            Expand-Archive -Path $Archive -DestinationPath $Extract
            $Source = (Get-ChildItem -Directory $Extract | Select-Object -First 1).FullName
        }
    }

    $Python = Find-Python
    $Cli = Join-Path $Source "bin/potetos"
    if (-not (Test-Path $Cli)) { throw "potetos: invalid source directory: $Source" }

    $Manifest = Join-Path $Target ".potetos/install.json"
    if ($Action -eq "auto") {
        $Action = if (Test-Path $Manifest) { "update" } else { "install" }
    }
    switch ($Action) {
        "install" { & $Python $Cli install --target $Target --agent $Agent }
        "update" {
            $Args = @($Cli, "update", "--target", $Target)
            if ($EphemeralSource) { $Args += "--copy" }
            if ($env:POTETOS_FORCE -eq "1") { $Args += "--force" }
            & $Python @Args
        }
        "uninstall" { & $Python $Cli uninstall --target $Target }
        "status" { & $Python $Cli status --target $Target }
        "doctor" { & $Python $Cli doctor --target $Target }
        default { throw "potetos: unknown bootstrap action: $Action" }
    }
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    if ($TempRoot -and (Test-Path $TempRoot)) { Remove-Item -Recurse -Force $TempRoot }
}
