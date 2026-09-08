$ErrorActionPreference = "Stop"

$Repository = if ($env:POTETOS_REPO) { $env:POTETOS_REPO } else { "TheOnlyFusionCube/potetos-for-everyone" }
$Ref = if ($env:POTETOS_REF) { $env:POTETOS_REF } else { "main" }
$Target = if ($env:POTETOS_TARGET) { $env:POTETOS_TARGET } else { (Get-Location).Path }
$Agent = if ($env:POTETOS_AGENT) { $env:POTETOS_AGENT } else { "all" }
$Action = if ($env:POTETOS_ACTION) { $env:POTETOS_ACTION } else { "auto" }
$Source = $env:POTETOS_SOURCE_DIR
$TempRoot = $null
$EphemeralSource = $false

function Find-Runner {
    if (Get-Command node -ErrorAction SilentlyContinue) { return "node" }
    foreach ($candidate in @("python3", "python", "py")) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) { return $candidate }
    }
    return "powershell"
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

    $Manifest = Join-Path $Target ".potetos/install.json"
    if ($Action -eq "auto") {
        $Action = if (Test-Path $Manifest) { "update" } else { "install" }
    }

    $Runner = Find-Runner
    if ($Runner -eq "node") {
        $Cli = Join-Path $Source "npm/potetos.mjs"
        switch ($Action) {
            "install" { & node $Cli install --target $Target --agent $Agent }
            "update" {
                $Args = @($Cli, "update", "--target", $Target)
                if ($env:POTETOS_FORCE -eq "1") { $Args += "--force" }
                & node @Args
            }
            "uninstall" { & node $Cli uninstall --target $Target }
            "status" { & node $Cli status --target $Target }
            "doctor" { & node $Cli doctor --target $Target }
            default { throw "potetos: unknown action: $Action" }
        }
    } elseif ($Runner -in @("python3", "python", "py")) {
        $Cli = Join-Path $Source "bin/potetos"
        switch ($Action) {
            "install" { & $Runner $Cli install --target $Target --agent $Agent }
            "update" {
                $Args = @($Cli, "update", "--target", $Target)
                if ($EphemeralSource) { $Args += "--copy" }
                if ($env:POTETOS_FORCE -eq "1") { $Args += "--force" }
                & $Runner @Args
            }
            "uninstall" { & $Runner $Cli uninstall --target $Target }
            "status" { & $Runner $Cli status --target $Target }
            "doctor" { & $Runner $Cli doctor --target $Target }
            default { throw "potetos: unknown action: $Action" }
        }
    } else {
        # Native PowerShell fallback
        $SkillsDst = Join-Path $Target ".agents/skills"
        switch ($Action) {
            "install" {
                New-Item -ItemType Directory -Force -Path $SkillsDst | Out-Null
                Copy-Item -Recurse -Force (Join-Path $Source "skills/*") $SkillsDst
                $PotetosDir = Join-Path $Target ".potetos"
                New-Item -ItemType Directory -Force -Path $PotetosDir | Out-Null
                '{"mode": "copy", "skills": ".agents/skills", "installer": "powershell"}' | Out-File -Encoding utf8 (Join-Path $PotetosDir "install.json")
                $AgentsMd = Join-Path $Target "AGENTS.md"
                "`n<!-- potetos-for-everyone:begin -->`n## potetos-for-everyone`n`nFor non-trivial engineering work, use the Agent Skill at `.agents/skills/poteto-mode/SKILL.md`.`n<!-- potetos-for-everyone:end -->`n" | Out-File -Append -Encoding utf8 $AgentsMd
                Write-Host "installed skills in $Target"
                Write-Host "ready: ask your agent to use poteto-mode"
            }
            "uninstall" {
                if (Test-Path $SkillsDst) { Remove-Item -Recurse -Force $SkillsDst }
                if (Test-Path (Join-Path $Target ".potetos")) { Remove-Item -Recurse -Force (Join-Path $Target ".potetos") }
                Write-Host "uninstalled potetos-for-everyone from $Target"
            }
            default { throw "potetos: $Action requires Node.js or Python." }
        }
    }
}
finally {
    if ($TempRoot -and (Test-Path $TempRoot)) { Remove-Item -Recurse -Force $TempRoot }
}
