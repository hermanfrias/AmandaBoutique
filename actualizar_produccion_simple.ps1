# Script simplificado para actualizar Amanda Boutique en producción
# Ejecutar desde el equipo de desarrollo
# NOTA: Requiere acceso de red al servidor (\\192.168.1.193\AmandaBoutique)

Write-Host "=== Actualizando Amanda Boutique en Producción ===" -ForegroundColor Green
Write-Host ""

# Configuración
$desarrollo = "E:\AmandaBoutique desarrollo"
$produccion = "\\192.168.1.193\AmandaBoutique"

# 1. Verificar que el desarrollo funciona
Write-Host "1. Verificando proyecto de desarrollo..." -ForegroundColor Yellow
cd $desarrollo
py manage.py check
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ✗ Error: El proyecto tiene problemas. Revisa antes de continuar." -ForegroundColor Red
    pause
    exit 1
}
Write-Host "   ✓ Proyecto OK" -ForegroundColor Green
Write-Host ""

# 2. Backup de producción
Write-Host "2. Haciendo backup de producción..." -ForegroundColor Yellow
$backupDate = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupPath = "$produccion\backups"

# Crear carpeta de backups si no existe
if (!(Test-Path $backupPath)) {
    New-Item -ItemType Directory -Path $backupPath | Out-Null
}

# Backup de la base de datos
if (Test-Path "$produccion\db.sqlite3") {
    Copy-Item "$produccion\db.sqlite3" "$backupPath\db_$backupDate.sqlite3"
    Write-Host "   ✓ Backup guardado: db_$backupDate.sqlite3" -ForegroundColor Green
} else {
    Write-Host "   ! No se encontró db.sqlite3 en producción" -ForegroundColor Yellow
}
Write-Host ""

# 3. Mensaje para detener servicio manualmente
Write-Host "3. DETÉN EL SERVICIO EN EL SERVIDOR" -ForegroundColor Red
Write-Host "   En el servidor (192.168.1.193), ejecuta:" -ForegroundColor Cyan
Write-Host "   nssm stop AmandaBoutique" -ForegroundColor White
Write-Host ""
Write-Host "   Presiona cualquier tecla cuando hayas detenido el servicio..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

# 4. Copiar archivos
Write-Host "4. Copiando archivos actualizados..." -ForegroundColor Yellow
Write-Host "   Esto puede tardar unos segundos..." -ForegroundColor Gray

# Excluir: .venv, __pycache__, .git, staticfiles, media, backups, .gemini
# Excluir archivos: *.pyc, db.sqlite3, .env
robocopy $desarrollo $produccion /MIR `
    /XD .venv __pycache__ .git staticfiles media backups .gemini `
    /XF *.pyc db.sqlite3 .env `
    /NFL /NDL /NP

Write-Host "   ✓ Archivos copiados" -ForegroundColor Green
Write-Host ""

# 5. Instrucciones para ejecutar en el servidor
Write-Host "5. EJECUTA LO SIGUIENTE EN EL SERVIDOR:" -ForegroundColor Red
Write-Host ""
Write-Host "   cd C:\AmandaBoutique" -ForegroundColor White
Write-Host "   .venv\Scripts\activate" -ForegroundColor White
Write-Host "   py manage.py migrate" -ForegroundColor White
Write-Host "   py manage.py collectstatic --noinput" -ForegroundColor White
Write-Host "   deactivate" -ForegroundColor White
Write-Host "   nssm start AmandaBoutique" -ForegroundColor White
Write-Host ""
Write-Host "   Presiona cualquier tecla cuando hayas completado estos pasos..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

Write-Host "=== Actualización completada ===" -ForegroundColor Green
Write-Host ""
Write-Host "Verifica que el sitio funciona en: http://192.168.1.193:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
