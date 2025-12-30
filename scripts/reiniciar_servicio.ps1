# Script de Reinicio del Servicio Django Amanda Boutique
# Ejecutar como Administrador

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🔧 Reinicio del Servicio Django Amanda Boutique" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# 1. Verificar estado actual del servicio
Write-Host "📊 Verificando estado del servicio..." -ForegroundColor Yellow
$service = Get-Service -Name "DjangoServidor" -ErrorAction SilentlyContinue

if ($null -eq $service) {
    Write-Host "❌ ERROR: El servicio 'DjangoServidor' no existe" -ForegroundColor Red
    Write-Host "   Por favor, verifica que NSSM esté instalado correctamente" -ForegroundColor Red
    exit 1
}

Write-Host "   Estado actual: $($service.Status)" -ForegroundColor White
Write-Host ""

# 2. Detener el servicio
Write-Host "🛑 Deteniendo el servicio..." -ForegroundColor Yellow
try {
    Stop-Service -Name "DjangoServidor" -Force -ErrorAction Stop
    Start-Sleep -Seconds 2
    Write-Host "   ✅ Servicio detenido correctamente" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Advertencia: $($_.Exception.Message)" -ForegroundColor Yellow
}
Write-Host ""

# 3. Verificar que se detuvo
$service = Get-Service -Name "DjangoServidor"
if ($service.Status -ne "Stopped") {
    Write-Host "   ⚠️  El servicio no se detuvo completamente, esperando..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}

# 4. Iniciar el servicio
Write-Host "🚀 Iniciando el servicio..." -ForegroundColor Yellow
try {
    Start-Service -Name "DjangoServidor" -ErrorAction Stop
    Start-Sleep -Seconds 3
    Write-Host "   ✅ Servicio iniciado correctamente" -ForegroundColor Green
} catch {
    Write-Host "   ❌ ERROR al iniciar el servicio: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Revisa los logs para más detalles" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 5. Verificar estado final
Write-Host "📊 Verificando estado final..." -ForegroundColor Yellow
$service = Get-Service -Name "DjangoServidor"
Write-Host "   Estado: $($service.Status)" -ForegroundColor White
Write-Host ""

# 6. Mostrar logs recientes
Write-Host "📄 Últimas líneas del log de salida:" -ForegroundColor Yellow
$outputLog = "E:\AmandaBoutique\logs\service_output.log"
if (Test-Path $outputLog) {
    Get-Content $outputLog -Tail 15 | ForEach-Object {
        Write-Host "   $_" -ForegroundColor Gray
    }
} else {
    Write-Host "   ⚠️  No se encontró el archivo de log: $outputLog" -ForegroundColor Yellow
}
Write-Host ""

# 7. Verificar errores
Write-Host "⚠️  Verificando errores:" -ForegroundColor Yellow
$errorLog = "E:\AmandaBoutique\logs\service_error.log"
if (Test-Path $errorLog) {
    $errors = Get-Content $errorLog -Tail 10
    if ($errors.Count -gt 0) {
        Write-Host "   ⚠️  Se encontraron errores recientes:" -ForegroundColor Red
        $errors | ForEach-Object {
            Write-Host "   $_" -ForegroundColor Red
        }
    } else {
        Write-Host "   ✅ No hay errores recientes" -ForegroundColor Green
    }
} else {
    Write-Host "   ⚠️  No se encontró el archivo de errores: $errorLog" -ForegroundColor Yellow
}
Write-Host ""

# 8. Obtener IP del servidor
Write-Host "🌐 Información de red:" -ForegroundColor Yellow
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" }).IPAddress
if ($ipAddress) {
    Write-Host "   📍 IP Local: $ipAddress" -ForegroundColor White
    Write-Host "   🌐 URL: http://$ipAddress:8000" -ForegroundColor Cyan
} else {
    Write-Host "   ⚠️  No se pudo determinar la IP local" -ForegroundColor Yellow
}
Write-Host ""

# 9. Verificar firewall
Write-Host "🔥 Verificando regla de firewall:" -ForegroundColor Yellow
$firewallRule = Get-NetFirewallRule -DisplayName "Django Amanda Boutique" -ErrorAction SilentlyContinue
if ($null -eq $firewallRule) {
    Write-Host "   ⚠️  ADVERTENCIA: No existe regla de firewall" -ForegroundColor Red
    Write-Host "   Ejecuta el siguiente comando como Administrador:" -ForegroundColor Yellow
    Write-Host '   New-NetFirewallRule -DisplayName "Django Amanda Boutique" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow -Profile Domain,Private' -ForegroundColor Cyan
} else {
    Write-Host "   ✅ Regla de firewall configurada: $($firewallRule.Enabled)" -ForegroundColor Green
}
Write-Host ""

# 10. Resumen final
Write-Host "=" * 60 -ForegroundColor Cyan
if ($service.Status -eq "Running") {
    Write-Host "✅ SERVICIO FUNCIONANDO CORRECTAMENTE" -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes acceder al sistema desde:" -ForegroundColor White
    Write-Host "  • Servidor local: http://localhost:8000" -ForegroundColor Cyan
    if ($ipAddress) {
        Write-Host "  • Red local: http://$ipAddress:8000" -ForegroundColor Cyan
    }
} else {
    Write-Host "❌ EL SERVICIO NO ESTÁ FUNCIONANDO" -ForegroundColor Red
    Write-Host "   Revisa los logs para más información" -ForegroundColor Yellow
}
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
