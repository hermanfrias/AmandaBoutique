# Plan de Producción - Amanda Mateo Boutique

## Versión 3.0 - Windows 11 + NSSM (Red Local)

**Fecha**: 21 de diciembre de 2025  
**Entorno**: Windows 11  
**Servidor**: NSSM (Non-Sucking Service Manager)  
**Red**: Local (LAN)

---

## 📋 Resumen Ejecutivo

Este plan detalla el despliegue del sistema Amanda Mateo Boutique v3.0 en un servidor Windows 11 usando NSSM para ejecutar Django como servicio de Windows en red local.

**Estado actual**: Desarrollo completado y probado localmente  
**Base de datos**: Se mantendrá la BD actual (SQLite - ya actualizada)  
**Objetivo**: Configurar servicio Windows con NSSM para acceso en red local

---

## 🎯 Arquitectura del Despliegue

```
Servidor Windows 11
├── Python 3.11+ (con venv)
├── Django 5.2.7
├── Waitress (Servidor WSGI)
├── NSSM (Gestor de Servicios)
└── SQLite Database
```

**Acceso en red local:**

- IP del servidor: `192.168.1.X` (tu IP local)
- Puerto: `8000` (configurable)
- URL: `http://192.168.1.X:8000`

---

## ✅ Requisitos Previos

### Software Necesario

- [x] Windows 11 (ya instalado)
- [x] Python 3.11 o superior
- [x] Git (opcional, para control de versiones)
- [x] NSSM (Non-Sucking Service Manager)

### Descargas

**NSSM:**

- URL: https://nssm.cc/download
- Versión recomendada: 2.24 (última estable)
- Descargar: `nssm-2.24.zip`

---

## 🚀 Fase 1: Preparación del Entorno

### 1.1 Verificar Python

```powershell
# Verificar versión de Python
python --version
# Debe mostrar: Python 3.11.x o superior

# Verificar pip
pip --version
```

### 1.2 Descargar e Instalar NSSM

```powershell
# Opción 1: Descargar manualmente
# 1. Ir a https://nssm.cc/download
# 2. Descargar nssm-2.24.zip
# 3. Extraer a C:\nssm

# Opción 2: Con PowerShell (si tienes wget)
wget https://nssm.cc/release/nssm-2.24.zip -OutFile nssm.zip
Expand-Archive nssm.zip -DestinationPath C:\nssm

# Agregar NSSM al PATH (opcional)
# Panel de Control > Sistema > Configuración avanzada > Variables de entorno
# Agregar: C:\nssm\win64 (o win32 según tu sistema)
```

### 1.3 Configurar Firewall de Windows

```powershell
# Abrir PowerShell como Administrador

# Crear regla de firewall para el puerto 8000
New-NetFirewallRule -DisplayName "Django Amanda Boutique" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 8000 `
    -Action Allow `
    -Profile Domain,Private

# Verificar regla creada
Get-NetFirewallRule -DisplayName "Django Amanda Boutique"
```

---

## 📦 Fase 2: Preparar el Proyecto

### 2.1 Ubicación del Proyecto

**Ruta recomendada**: `E:\AmandaBoutique` (producción)

```powershell
# Si estás en desarrollo en otra carpeta, copiar a producción
# Desde: E:\AmandaBoutique desarrollo
# Hacia: E:\AmandaBoutique

# Copiar proyecto (excluyendo archivos innecesarios)
robocopy "E:\AmandaBoutique desarrollo" "E:\AmandaBoutique" /E /XD .venv __pycache__ .git /XF *.pyc *.log
```

**Nota**: Si ya tienes el proyecto en `E:\AmandaBoutique`, puedes trabajar directamente ahí.

### 2.2 Crear Entorno Virtual

```powershell
cd E:\AmandaBoutique

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Si hay error de ejecución de scripts, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2.3 Instalar Dependencias

```powershell
# Asegurarse de que el venv está activado
# Debe aparecer (.venv) al inicio del prompt

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Instalar Waitress (servidor WSGI para Windows)
pip install waitress
```

### 2.4 Copiar Base de Datos

```powershell
# Si la BD está en desarrollo, copiarla a producción
copy "E:\AmandaBoutique desarrollo\db.sqlite3" "E:\AmandaBoutique\db.sqlite3"

# Verificar que existe
dir db.sqlite3
```

### 2.5 Copiar Archivos Media

```powershell
# Copiar carpeta media completa
robocopy "E:\AmandaBoutique desarrollo\media" "E:\AmandaBoutique\media" /E
```

---

## ⚙️ Fase 3: Configurar Django para Producción

### 3.1 Crear Archivo de Configuración de Producción

Crear archivo: `E:\AmandaBoutique\AmandaProjecto\settings_prod.py`

```python
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Permitir acceso desde la red local
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.*',  # Permite cualquier IP en la red local
    # O especificar IPs exactas:
    # '192.168.1.100',  # IP del servidor
    # '192.168.1.101',  # Otra PC en la red
]

# Base de datos (mantener SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings (opcional para red local)
# SECURE_SSL_REDIRECT = False  # No usar HTTPS en red local
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False

# CSRF trusted origins (agregar IP del servidor)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://192.168.1.193:8000',  # Cambiar por tu IP
]
```

### 3.2 Recolectar Archivos Estáticos

```powershell
# Activar entorno virtual si no está activo
.\.venv\Scripts\Activate.ps1

# Configurar variable de entorno
$env:DJANGO_SETTINGS_MODULE = "AmandaProjecto.settings_prod"

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### 3.3 Aplicar Migraciones (si es necesario)

```powershell
# Verificar migraciones pendientes
python manage.py showmigrations

# Aplicar migraciones si hay pendientes
python manage.py migrate
```

---

## 🔧 Fase 4: Crear Script de Servidor

### 4.1 Crear `server.py`

Crear archivo: `E:\AmandaBoutique\server.py`

```python
import os
import sys
from waitress import serve

# Configurar settings de producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AmandaProjecto.settings_prod')

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

# Importar la aplicación WSGI
from AmandaProjecto.wsgi import application

if __name__ == '__main__':
    # Obtener IP del servidor
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("=" * 60)
    print("🚀 Servidor Amanda Boutique Iniciado")
    print("=" * 60)
    print(f"📍 IP Local: {local_ip}")
    print(f"🌐 URL Local: http://{local_ip}:8000")
    print(f"🏠 URL Localhost: http://localhost:8000")
    print("=" * 60)
    print("⚠️  Presiona CTRL+C para detener el servidor")
    print("=" * 60)

    # Iniciar servidor Waitress
    serve(
        application,
        host='0.0.0.0',  # Escuchar en todas las interfaces
        port=8000,
        threads=4,  # Número de threads
        url_scheme='http'
    )
```

### 4.2 Probar el Servidor Manualmente

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar servidor
python server.py

# Deberías ver:
# ============================================================
# 🚀 Servidor Amanda Boutique Iniciado
# ============================================================
# 📍 IP Local: 192.168.1.X
# 🌐 URL Local: http://192.168.1.X:8000
# ...

# Probar en navegador:
# - http://localhost:8000
# - http://192.168.1.X:8000 (desde otra PC en la red)

# Detener con CTRL+C
```

---

## 🎯 Fase 5: Configurar Servicio con NSSM

### 5.1 Instalar Servicio con NSSM

```powershell
# Abrir PowerShell como Administrador
# Navegar a la carpeta de NSSM
cd C:\nssm\win64

# Instalar servicio (abre GUI)
.\nssm.exe install DjangoAmandaBoutique
```

### 5.2 Configurar Servicio en GUI de NSSM

**Pestaña "Application":**

| Campo             | Valor                                        |
| ----------------- | -------------------------------------------- |
| Path              | `E:\AmandaBoutique\.venv\Scripts\python.exe` |
| Startup directory | `E:\AmandaBoutique`                          |
| Arguments         | `server.py`                                  |

**Pestaña "Details":**

| Campo        | Valor                                             |
| ------------ | ------------------------------------------------- |
| Display name | `Amanda Boutique - Django Server`                 |
| Description  | `Servidor Django para Amanda Mateo Boutique v3.0` |
| Startup type | `Automatic`                                       |

**Pestaña "Log on":**

- Dejar en "Local System account" (o configurar usuario específico)

**Pestaña "I/O":**

| Campo           | Valor                                       |
| --------------- | ------------------------------------------- |
| Output (stdout) | `E:\AmandaBoutique\logs\service_output.log` |
| Error (stderr)  | `E:\AmandaBoutique\logs\service_error.log`  |

**Nota**: Crear carpeta de logs antes:

```powershell
mkdir E:\AmandaBoutique\logs
```

### 5.3 Configurar con Línea de Comandos (Alternativa)

```powershell
# Si prefieres configurar por comandos en lugar de GUI

cd C:\nssm\win64

# Instalar servicio
.\nssm.exe install DjangoAmandaBoutique "E:\AmandaBoutique\.venv\Scripts\python.exe" "server.py"

# Configurar directorio de trabajo
.\nssm.exe set DjangoAmandaBoutique AppDirectory "E:\AmandaBoutique"

# Configurar logs
.\nssm.exe set DjangoAmandaBoutique AppStdout "E:\AmandaBoutique\logs\service_output.log"
.\nssm.exe set DjangoAmandaBoutique AppStderr "E:\AmandaBoutique\logs\service_error.log"

# Configurar inicio automático
.\nssm.exe set DjangoAmandaBoutique Start SERVICE_AUTO_START

# Configurar descripción
.\nssm.exe set DjangoAmandaBoutique Description "Servidor Django para Amanda Mateo Boutique v3.0"
```

### 5.4 Iniciar Servicio

```powershell
# Opción 1: Con NSSM
cd C:\nssm\win64
.\nssm.exe start DjangoAmandaBoutique

# Opción 2: Con PowerShell
Start-Service DjangoAmandaBoutique

# Opción 3: Con GUI de Windows
# Servicios (services.msc) > Buscar "Amanda Boutique" > Iniciar
```

### 5.5 Verificar Estado del Servicio

```powershell
# Ver estado
Get-Service DjangoAmandaBoutique

# Ver logs
Get-Content E:\AmandaBoutique\logs\service_output.log -Tail 20

# Ver errores
Get-Content E:\AmandaBoutique\logs\service_error.log -Tail 20
```

---

## 🧪 Fase 6: Pruebas y Verificación

### 6.1 Obtener IP del Servidor

```powershell
# Ver IP del servidor
ipconfig

# Buscar "Adaptador de Ethernet" o "Adaptador de LAN inalámbrica"
# Anotar la "Dirección IPv4": 192.168.1.X
```

### 6.2 Checklist de Verificación

**En el servidor:**

- [ ] Servicio "DjangoAmandaBoutique" está corriendo
- [ ] Logs no muestran errores
- [ ] http://localhost:8000 funciona
- [ ] http://192.168.1.X:8000 funciona

**Desde otra PC en la red:**

- [ ] Puede acceder a http://192.168.1.X:8000
- [ ] Login funciona correctamente
- [ ] Todos los módulos cargan sin errores
- [ ] Imágenes y archivos media se muestran
- [ ] Archivos estáticos (CSS, JS) cargan
- [ ] Formularios funcionan (crear, editar, eliminar)
- [ ] Exportación a PDF funciona
- [ ] Permisos de usuario funcionan

### 6.3 Pruebas de Funcionalidad

1. **Login y Autenticación**

   - Iniciar sesión con superusuario
   - Crear usuario nuevo
   - Editar permisos de usuario
   - Cerrar sesión

2. **Módulos Principales**

   - Crear/editar/eliminar en cada módulo
   - Verificar filtros y búsquedas
   - Probar exportación a PDF

3. **Gestión de Archivos**

   - Subir imagen de producto
   - Subir avatar de usuario
   - Verificar eliminación de archivos

4. **Responsividad**
   - Probar en móvil
   - Probar en tablet
   - Probar en desktop

---

## 💾 Fase 7: Configurar Backups Automáticos

### 7.1 Crear Script de Backup

Crear archivo: `E:\AmandaBoutique\backup_script.ps1`

```powershell
# Script de Backup para Amanda Boutique
# Ejecutar como Administrador

# Configuración
$BackupDir = "E:\Backups\AmandaBoutique"
$ProjectDir = "E:\AmandaBoutique"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"

# Crear directorio de backups si no existe
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir
}

Write-Host "🔄 Iniciando backup..." -ForegroundColor Cyan

# Backup de base de datos
Write-Host "📦 Respaldando base de datos..." -ForegroundColor Yellow
Copy-Item "$ProjectDir\db.sqlite3" "$BackupDir\db_$Date.sqlite3"

# Backup de archivos media
Write-Host "📸 Respaldando archivos media..." -ForegroundColor Yellow
$MediaBackup = "$BackupDir\media_$Date.zip"
Compress-Archive -Path "$ProjectDir\media\*" -DestinationPath $MediaBackup -Force

# Eliminar backups antiguos (más de 30 días)
Write-Host "🗑️  Eliminando backups antiguos..." -ForegroundColor Yellow
Get-ChildItem $BackupDir -Filter "db_*.sqlite3" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
    Remove-Item

Get-ChildItem $BackupDir -Filter "media_*.zip" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
    Remove-Item

Write-Host "✅ Backup completado: $Date" -ForegroundColor Green
Write-Host "📁 Ubicación: $BackupDir" -ForegroundColor Green
```

### 7.2 Programar Backup Automático con Tareas Programadas

```powershell
# Abrir PowerShell como Administrador

# Crear tarea programada para backup diario a las 2:00 AM
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-ExecutionPolicy Bypass -File E:\AmandaBoutique\backup_script.ps1"

$Trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM

$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "Backup Amanda Boutique" `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Settings $Settings `
    -Description "Backup diario de base de datos y archivos media"

# Verificar tarea creada
Get-ScheduledTask -TaskName "Backup Amanda Boutique"
```

### 7.3 Probar Backup Manualmente

```powershell
# Ejecutar backup manualmente
PowerShell.exe -ExecutionPolicy Bypass -File E:\AmandaBoutique\backup_script.ps1

# Verificar archivos creados
dir E:\Backups\AmandaBoutique
```

---

## 🔄 Fase 8: Mantenimiento y Actualización

### 8.1 Detener Servicio

```powershell
# Opción 1: Con PowerShell
Stop-Service DjangoAmandaBoutique

# Opción 2: Con NSSM
cd C:\nssm\win64
.\nssm.exe stop DjangoAmandaBoutique

# Verificar que se detuvo
Get-Service DjangoAmandaBoutique
```

### 8.2 Actualizar Proyecto

```powershell
# 1. Detener servicio
Stop-Service DjangoAmandaBoutique

# 2. Activar entorno virtual
cd E:\AmandaBoutique
.\.venv\Scripts\Activate.ps1

# 3. Actualizar código (si usas Git)
git pull origin main

# O copiar archivos manualmente desde desarrollo
# robocopy "E:\AmandaBoutique desarrollo" "E:\AmandaBoutique" /E /XD .venv __pycache__ /XF *.pyc

# 4. Instalar nuevas dependencias (si hay)
pip install -r requirements.txt

# 5. Aplicar migraciones (si hay)
python manage.py migrate

# 6. Recolectar estáticos
python manage.py collectstatic --noinput

# 7. Reiniciar servicio
Start-Service DjangoAmandaBoutique
```

### 8.3 Ver Logs del Servicio

```powershell
# Ver últimas 50 líneas del log
Get-Content E:\AmandaBoutique\logs\service_output.log -Tail 50

# Ver errores
Get-Content E:\AmandaBoutique\logs\service_error.log -Tail 50

# Monitorear en tiempo real
Get-Content E:\AmandaBoutique\logs\service_output.log -Wait
```

### 8.4 Reiniciar Servicio

```powershell
# Reiniciar servicio
Restart-Service DjangoAmandaBoutique

# O con NSSM
cd C:\nssm\win64
.\nssm.exe restart DjangoAmandaBoutique
```

---

## 🆘 Solución de Problemas Comunes

### Problema 1: Servicio no inicia

**Síntomas**: Servicio se detiene inmediatamente después de iniciar

**Solución**:

```powershell
# Ver logs de error
Get-Content E:\AmandaBoutique\logs\service_error.log

# Verificar que el path de Python es correcto
cd C:\nssm\win64
.\nssm.exe get DjangoAmandaBoutique Application

# Probar ejecutar manualmente
cd E:\AmandaBoutique
.\.venv\Scripts\Activate.ps1
python server.py
```

### Problema 2: No se puede acceder desde otra PC

**Síntomas**: Funciona en localhost pero no desde la red

**Solución**:

```powershell
# 1. Verificar firewall
Get-NetFirewallRule -DisplayName "Django Amanda Boutique"

# 2. Verificar que el servidor escucha en 0.0.0.0
# En server.py debe tener: host='0.0.0.0'

# 3. Verificar IP del servidor
ipconfig

# 4. Probar conectividad desde otra PC
# En otra PC, abrir CMD y ejecutar:
ping 192.168.1.X
telnet 192.168.1.X 8000
```

### Problema 3: Archivos estáticos no cargan

**Síntomas**: Página sin estilos CSS

**Solución**:

```powershell
# Recolectar estáticos nuevamente
cd E:\AmandaBoutique
.\.venv\Scripts\Activate.ps1
python manage.py collectstatic --noinput

# Verificar que existe la carpeta
dir staticfiles

# Reiniciar servicio
Restart-Service DjangoAmandaBoutique
```

### Problema 4: Error de permisos en base de datos

**Síntomas**: "database is locked" o errores de escritura

**Solución**:

```powershell
# Verificar permisos de la carpeta
icacls E:\AmandaBoutique\db.sqlite3

# Dar permisos completos
icacls E:\AmandaBoutique\db.sqlite3 /grant Everyone:F

# O configurar el servicio para correr con tu usuario
cd C:\nssm\win64
.\nssm.exe set DjangoAmandaBoutique ObjectName ".\TU_USUARIO" "TU_CONTRASEÑA"
```

### Problema 5: Servicio se detiene solo

**Síntomas**: Servicio funciona pero se detiene después de un tiempo

**Solución**:

```powershell
# Configurar recuperación automática
cd C:\nssm\win64

# Reiniciar en caso de fallo
.\nssm.exe set DjangoAmandaBoutique AppExit Default Restart

# Delay de 5 segundos antes de reiniciar
.\nssm.exe set DjangoAmandaBoutique AppRestartDelay 5000

# Ver configuración
.\nssm.exe get DjangoAmandaBoutique AppExit
```

---

## 📊 Comandos Útiles de NSSM

```powershell
cd C:\nssm\win64

# Ver estado del servicio
.\nssm.exe status DjangoAmandaBoutique

# Iniciar servicio
.\nssm.exe start DjangoAmandaBoutique

# Detener servicio
.\nssm.exe stop DjangoAmandaBoutique

# Reiniciar servicio
.\nssm.exe restart DjangoAmandaBoutique

# Editar configuración (abre GUI)
.\nssm.exe edit DjangoAmandaBoutique

# Ver toda la configuración
.\nssm.exe dump DjangoAmandaBoutique

# Desinstalar servicio
.\nssm.exe remove DjangoAmandaBoutique confirm
```

---

## ✅ Checklist Final de Producción

### Configuración Inicial

- [ ] Python 3.11+ instalado
- [ ] NSSM descargado y configurado
- [ ] Firewall configurado (puerto 8000)
- [ ] Proyecto copiado a `E:\AmandaBoutique`
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Waitress instalado

### Configuración de Django

- [ ] `settings_prod.py` creado
- [ ] `ALLOWED_HOSTS` configurado con IPs de red
- [ ] Base de datos copiada
- [ ] Archivos media copiados
- [ ] Archivos estáticos recolectados
- [ ] Migraciones aplicadas

### Configuración de Servicio

- [ ] `server.py` creado
- [ ] Servicio NSSM instalado
- [ ] Servicio configurado correctamente
- [ ] Carpeta de logs creada
- [ ] Servicio iniciado
- [ ] Inicio automático configurado

### Backups

- [ ] Script de backup creado
- [ ] Tarea programada configurada
- [ ] Backup manual probado
- [ ] Carpeta de backups creada

### Pruebas

- [ ] Acceso desde localhost funciona
- [ ] Acceso desde red local funciona
- [ ] Login funciona
- [ ] Todos los módulos cargan
- [ ] Imágenes se muestran
- [ ] CSS/JS cargan correctamente
- [ ] Formularios funcionan
- [ ] PDF se genera
- [ ] Permisos funcionan

### Documentación

- [ ] IP del servidor documentada
- [ ] Credenciales de superusuario guardadas
- [ ] Procedimiento de backup documentado
- [ ] Procedimiento de actualización documentado

---

## 📞 Información de Contacto y Soporte

**IP del Servidor**: `192.168.1.___` (completar)  
**Puerto**: `8000`  
**URL**: `http://192.168.1.___:8000`

**Ubicación del Proyecto**: `E:\AmandaBoutique`  
**Ubicación de Backups**: `E:\Backups\AmandaBoutique`  
**Logs**: `E:\AmandaBoutique\logs\`

**Servicio Windows**: `DjangoAmandaBoutique`  
**Comando para reiniciar**: `Restart-Service DjangoAmandaBoutique`

---

**Fecha de creación**: 21 de diciembre de 2025  
**Versión del plan**: 2.0 (Windows 11 + NSSM)  
**Proyecto**: Amanda Mateo Boutique v3.0  
**Entorno**: Windows 11 - Red Local
