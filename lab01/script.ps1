# Ejecuta el Lab 01 completo. Uso (desde cualquier carpeta):
#   powershell -ExecutionPolicy Bypass -File .\script.ps1

Set-Location $PSScriptRoot
$env:PYTHONUTF8 = 1   # evita los acentos rotos en consola

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv no esta instalado (paso A1 del lab)." -ForegroundColor Red
    exit 1
}

$pasos = @(
    @{ Titulo = "Descobrir a maquina (cores, RAM, GIL)"; Script = "descobrir_maquina.py" },
    @{ Titulo = "Medir CPU-bound vs I/O-bound";           Script = "medir.py" },
    @{ Titulo = "Demo: 1 core vs todos os cores";        Script = "demo_docente.py" },
    @{ Titulo = "Verificador do Lab 01";                 Script = "verificar_lab01.py" }
)

$falhas = @()
foreach ($paso in $pasos) {
    Write-Host "`n=== $($paso.Titulo) ===" -ForegroundColor Cyan
    uv run python $paso.Script
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FALHOU: $($paso.Script) (código $LASTEXITCODE)" -ForegroundColor Red
        $falhas += $paso.Script
    }
}

Write-Host ""
if ($falhas.Count -eq 0) {
    Write-Host "Todos os passos terminaram sem erro." -ForegroundColor Green
    exit 0
}
Write-Host "Passos com erro: $($falhas -join ', ')" -ForegroundColor Red
exit 1
