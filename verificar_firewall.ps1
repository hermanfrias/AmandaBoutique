# Script de Verificación de Firewall para Django Amanda Boutique
# Ejecutar como Administrador

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🔥 Verificación y Configuración de Firewall" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# 1. Verificar si existe la regla
Write-Host "📊 Verificando regla de firewall existente..." -ForegroundColor Yellow
$firewallRule = Get-NetFirewallRule -DisplayName "Django Amanda Boutique" -ErrorAction SilentlyContinue

if ($null -eq $firewallRule) {
    Write-Host "   ❌ No existe regla de firewall" -ForegroundColor Red
    Write-Host ""
    
    # 2. Crear regla de firewall
    Write-Host "🔧 Creando regla de firewall..." -ForegroundColor Yellow
    try {
        New-NetFirewallRule -DisplayName "Django Amanda Boutique" `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort 8000 `
            -Action Allow `
            -Profile Domain,Private `
            -ErrorAction Stop
        
        Write-Host "   ✅ Regla de firewall creada correctamente" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ ERROR al crear regla: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ✅ Regla de firewall ya existe" -ForegroundColor Green
    
    # Mostrar detalles de la regla
    Write-Host ""
    Write-Host "📋 Detalles de la regla:" -ForegroundColor Yellow
    Write-Host "   Nombre: $($firewallRule.DisplayName)" -ForegroundColor White
    Write-Host "   Habilitada: $($firewallRule.Enabled)" -ForegroundColor White
    Write-Host "   Dirección: $($firewallRule.Direction)" -ForegroundColor White
    Write-Host "   Acción: $($firewallRule.Action)" -ForegroundColor White
    
    # Verificar si está habilitada
    if ($firewallRule.Enabled -eq $false) {
        Write-Host ""
        Write-Host "   ⚠️  La regla está DESHABILITADA" -ForegroundColor Red
        Write-Host "   Habilitando regla..." -ForegroundColor Yellow
        
        try {
            Enable-NetFirewallRule -DisplayName "Django Amanda Boutique" -ErrorAction Stop
            Write-Host "   ✅ Regla habilitada correctamente" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ ERROR al habilitar regla: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host ""

# 3. Verificar puerto 8000
Write-Host "🔍 Verificando si el puerto 8000 está en uso..." -ForegroundColor Yellow
$connections = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($connections) {
    Write-Host "   ✅ Puerto 8000 está en uso (servidor corriendo)" -ForegroundColor Green
    $connections | ForEach-Object {
        Write-Host "   Estado: $($_.State) | Proceso: $(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)" -ForegroundColor White
    }
} else {
    Write-Host "   ⚠️  Puerto 8000 no está en uso (servidor detenido)" -ForegroundColor Yellow
}

Write-Host ""

# 4. Probar conectividad local
Write-Host "🌐 Probando conectividad local..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "   ✅ Servidor responde en localhost:8000" -ForegroundColor Green
    Write-Host "   Código de estado: $($response.StatusCode)" -ForegroundColor White
} catch {
    Write-Host "   ❌ No se puede conectar a localhost:8000" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 5. Obtener IP local
Write-Host "📍 Información de red:" -ForegroundColor Yellow
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress

if ($ipAddress) {
    Write-Host "   IP Local: $ipAddress" -ForegroundColor White
    Write-Host "   URL para otros equipos: http://$ipAddress:8000" -ForegroundColor Cyan
    
    # Probar conectividad con IP local
    Write-Host ""
    Write-Host "🌐 Probando conectividad con IP local..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://$ipAddress:8000" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        Write-Host "   ✅ Servidor responde en $ipAddress:8000" -ForegroundColor Green
        Write-Host "   Código de estado: $($response.StatusCode)" -ForegroundColor White
    } catch {
        Write-Host "   ❌ No se puede conectar a $ipAddress:8000" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "   ⚠️  No se pudo determinar la IP local" -ForegroundColor Yellow
}

Write-Host ""

# 6. Listar todas las reglas de firewall para el puerto 8000
Write-Host "📋 Todas las reglas de firewall para el puerto 8000:" -ForegroundColor Yellow
$allRules = Get-NetFirewallPortFilter -Protocol TCP | Where-Object { $_.LocalPort -eq 8000 } | Get-NetFirewallRule

if ($allRules) {
    $allRules | ForEach-Object {
        Write-Host "   • $($_.DisplayName) - Habilitada: $($_.Enabled) - Acción: $($_.Action)" -ForegroundColor White
    }
} else {
    Write-Host "   ⚠️  No hay reglas de firewall para el puerto 8000" -ForegroundColor Yellow
}

Write-Host ""

# 7. Resumen final
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "📊 RESUMEN" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

$firewallRule = Get-NetFirewallRule -DisplayName "Django Amanda Boutique" -ErrorAction SilentlyContinue
$service = Get-Service -Name "DjangoAmandaBoutique" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Firewall:" -ForegroundColor Yellow
if ($firewallRule -and $firewallRule.Enabled) {
    Write-Host "  ✅ Configurado correctamente" -ForegroundColor Green
} else {
    Write-Host "  ❌ Requiere configuración" -ForegroundColor Red
}

Write-Host ""
Write-Host "Servicio:" -ForegroundColor Yellow
if ($service -and $service.Status -eq "Running") {
    Write-Host "  ✅ Corriendo" -ForegroundColor Green
} else {
    Write-Host "  ❌ Detenido o no configurado" -ForegroundColor Red
}

Write-Host ""
Write-Host "Acceso:" -ForegroundColor Yellow
if ($ipAddress) {
    Write-Host "  • Desde este equipo: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  • Desde otros equipos: http://$ipAddress:8000" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
