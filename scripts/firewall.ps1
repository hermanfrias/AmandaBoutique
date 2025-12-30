# Script de Verificacion de Firewall
# IMPORTANTE: Ejecutar PowerShell como Administrador

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Verificacion de Firewall para Django" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar regla existente
Write-Host "1. Verificando regla de firewall..." -ForegroundColor Yellow
$firewallRule = Get-NetFirewallRule -DisplayName "Django Amanda Boutique" -ErrorAction SilentlyContinue

if ($null -eq $firewallRule) {
    Write-Host "   No existe regla de firewall" -ForegroundColor Red
    Write-Host ""
    Write-Host "2. Creando regla de firewall..." -ForegroundColor Yellow
    
    try {
        New-NetFirewallRule -DisplayName "Django Amanda Boutique" `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort 8000 `
            -Action Allow `
            -Profile Domain,Private
        
        Write-Host "   Regla creada correctamente" -ForegroundColor Green
    } catch {
        Write-Host "   ERROR: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   Regla de firewall existe" -ForegroundColor Green
    Write-Host "   Habilitada: $($firewallRule.Enabled)" -ForegroundColor White
    
    if ($firewallRule.Enabled -eq $false) {
        Write-Host ""
        Write-Host "2. Habilitando regla..." -ForegroundColor Yellow
        Enable-NetFirewallRule -DisplayName "Django Amanda Boutique"
        Write-Host "   Regla habilitada" -ForegroundColor Green
    }
}
Write-Host ""

# Verificar puerto
Write-Host "3. Verificando puerto 8000..." -ForegroundColor Yellow
$connections = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($connections) {
    Write-Host "   Puerto 8000 esta en uso (servidor corriendo)" -ForegroundColor Green
} else {
    Write-Host "   Puerto 8000 no esta en uso" -ForegroundColor Yellow
}
Write-Host ""

# Probar conectividad
Write-Host "4. Probando conectividad local..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "   Servidor responde en localhost:8000" -ForegroundColor Green
} catch {
    Write-Host "   No se puede conectar a localhost:8000" -ForegroundColor Red
}
Write-Host ""

# Obtener IP
Write-Host "5. Informacion de red:" -ForegroundColor Yellow
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress

if ($ipAddress) {
    Write-Host "   IP Local: $ipAddress" -ForegroundColor White
    Write-Host "   URL para otros equipos: http://$ipAddress:8000" -ForegroundColor Cyan
} else {
    Write-Host "   No se pudo determinar la IP local" -ForegroundColor Yellow
}
Write-Host ""

# Resumen
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "RESUMEN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$firewallRule = Get-NetFirewallRule -DisplayName "Django Amanda Boutique" -ErrorAction SilentlyContinue
$service = Get-Service -Name "DjangoServidor" -ErrorAction SilentlyContinue

Write-Host "Firewall:" -ForegroundColor Yellow
if ($firewallRule -and $firewallRule.Enabled) {
    Write-Host "  Configurado correctamente" -ForegroundColor Green
} else {
    Write-Host "  Requiere configuracion" -ForegroundColor Red
}
Write-Host ""

Write-Host "Servicio:" -ForegroundColor Yellow
if ($service -and $service.Status -eq "Running") {
    Write-Host "  Corriendo" -ForegroundColor Green
} else {
    Write-Host "  Detenido" -ForegroundColor Red
}
Write-Host ""

if ($ipAddress) {
    Write-Host "Acceso:" -ForegroundColor Yellow
    Write-Host "  - Desde este equipo: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  - Desde otros equipos: http://$ipAddress:8000" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
