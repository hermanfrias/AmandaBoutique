# Script Simple de Reinicio del Servicio Django
# IMPORTANTE: Ejecutar PowerShell como Administrador

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Reinicio del Servicio Django Amanda Boutique" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar estado actual
Write-Host "1. Verificando estado del servicio..." -ForegroundColor Yellow
$service = Get-Service -Name "DjangoServidor" -ErrorAction SilentlyContinue

if ($null -eq $service) {
    Write-Host "   ERROR: El servicio 'DjangoServidor' no existe" -ForegroundColor Red
    exit 1
}

Write-Host "   Estado actual: $($service.Status)" -ForegroundColor White
Write-Host ""

# Detener el servicio
Write-Host "2. Deteniendo el servicio..." -ForegroundColor Yellow
try {
    Stop-Service -Name "DjangoServidor" -Force
    Start-Sleep -Seconds 2
    Write-Host "   Servicio detenido" -ForegroundColor Green
} catch {
    Write-Host "   Advertencia: $($_.Exception.Message)" -ForegroundColor Yellow
}
Write-Host ""

# Iniciar el servicio
Write-Host "3. Iniciando el servicio con nueva configuracion..." -ForegroundColor Yellow
try {
    Start-Service -Name "DjangoServidor"
    Start-Sleep -Seconds 3
    Write-Host "   Servicio iniciado" -ForegroundColor Green
} catch {
    Write-Host "   ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Verificar estado final
Write-Host "4. Verificando estado final..." -ForegroundColor Yellow
$service = Get-Service -Name "DjangoServidor"
Write-Host "   Estado: $($service.Status)" -ForegroundColor White
Write-Host ""

# Mostrar logs si existen
Write-Host "5. Verificando logs..." -ForegroundColor Yellow
$outputLog = "E:\AmandaBoutique\logs\service_output.log"
if (Test-Path $outputLog) {
    Write-Host "   Ultimas lineas del log:" -ForegroundColor Gray
    Get-Content $outputLog -Tail 10 | ForEach-Object {
        Write-Host "   $_" -ForegroundColor Gray
    }
} else {
    Write-Host "   No se encontro archivo de log" -ForegroundColor Yellow
}
Write-Host ""

# Obtener IP
Write-Host "6. Informacion de red:" -ForegroundColor Yellow
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress
if ($ipAddress) {
    Write-Host "   IP Local: $ipAddress" -ForegroundColor White
    Write-Host "   URL: http://$ipAddress:8000" -ForegroundColor Cyan
}
Write-Host ""

# Resumen
Write-Host "============================================================" -ForegroundColor Cyan
if ($service.Status -eq "Running") {
    Write-Host "SERVICIO FUNCIONANDO CORRECTAMENTE" -ForegroundColor Green
    Write-Host ""
    Write-Host "Acceso desde:" -ForegroundColor White
    Write-Host "  - Servidor: http://localhost:8000" -ForegroundColor Cyan
    if ($ipAddress) {
        Write-Host "  - Red local: http://$ipAddress:8000" -ForegroundColor Cyan
    }
} else {
    Write-Host "EL SERVICIO NO ESTA FUNCIONANDO" -ForegroundColor Red
}
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
