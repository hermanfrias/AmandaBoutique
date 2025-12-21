# Plan de Producción - Amanda Mateo Boutique

## Versión 3.0 - Diciembre 2025

---

## 📋 Resumen Ejecutivo

Este documento detalla el plan completo para poner en producción el sistema Amanda Mateo Boutique versión 3.0, que incluye estandarización completa de UI/UX, responsividad total y nuevas funcionalidades de gestión de usuarios.

**Estado actual**: Desarrollo completado y probado localmente  
**Base de datos**: Se mantendrá la BD actual (ya actualizada)  
**Objetivo**: Despliegue en servidor de producción con mínimo downtime

---

## 🎯 Objetivos del Despliegue

1. ✅ Migrar código actualizado a producción
2. ✅ Mantener base de datos existente (sin pérdida de datos)
3. ✅ Configurar servidor web (Gunicorn + Nginx)
4. ✅ Implementar HTTPS con certificado SSL
5. ✅ Configurar archivos estáticos y media
6. ✅ Establecer sistema de backups automáticos
7. ✅ Documentar proceso de mantenimiento

---

## 📦 Requisitos Previos

### Servidor

- **Sistema Operativo**: Ubuntu 20.04 LTS o superior (recomendado)
- **RAM**: Mínimo 2GB (recomendado 4GB)
- **Disco**: Mínimo 20GB de espacio libre
- **Python**: 3.11 o superior
- **Acceso**: SSH con permisos sudo

### Dominio y DNS

- Dominio configurado apuntando al servidor
- Acceso a configuración DNS

### Herramientas Locales

- Git instalado
- Acceso al repositorio del proyecto
- Cliente FTP/SFTP (opcional, para transferencia de archivos)

---

## 🚀 Fase 1: Preparación del Servidor

### 1.1 Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 Instalar Dependencias del Sistema

```bash
# Python y herramientas
sudo apt install python3-pip python3-dev python3-venv -y

# Nginx (servidor web)
sudo apt install nginx -y

# PostgreSQL (recomendado para producción)
sudo apt install postgresql postgresql-contrib -y

# Dependencias para Pillow (manejo de imágenes)
sudo apt install libjpeg-dev zlib1g-dev -y

# Git
sudo apt install git -y
```

### 1.3 Configurar PostgreSQL (Recomendado)

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE amandaboutique;
CREATE USER amandauser WITH PASSWORD 'tu_contraseña_segura';
ALTER ROLE amandauser SET client_encoding TO 'utf8';
ALTER ROLE amandauser SET default_transaction_isolation TO 'read committed';
ALTER ROLE amandauser SET timezone TO 'America/Caracas';
GRANT ALL PRIVILEGES ON DATABASE amandaboutique TO amandauser;
\q
```

**Nota**: Si prefieres mantener SQLite, puedes omitir este paso, pero PostgreSQL es más robusto para producción.

---

## 📥 Fase 2: Despliegue del Código

### 2.1 Crear Directorio del Proyecto

```bash
sudo mkdir -p /var/www/amandaboutique
sudo chown $USER:$USER /var/www/amandaboutique
cd /var/www/amandaboutique
```

### 2.2 Clonar o Transferir el Proyecto

**Opción A: Con Git (Recomendado)**

```bash
git clone <url-del-repositorio> .
```

**Opción B: Transferencia Manual**

```bash
# Desde tu máquina local, comprimir el proyecto
cd "E:\AmandaBoutique desarrollo"
tar -czf amandaboutique.tar.gz --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' .

# Transferir al servidor (usar SCP o SFTP)
scp amandaboutique.tar.gz usuario@servidor:/var/www/amandaboutique/

# En el servidor, descomprimir
cd /var/www/amandaboutique
tar -xzf amandaboutique.tar.gz
rm amandaboutique.tar.gz
```

### 2.3 Transferir Base de Datos

**Si usas SQLite (mantener BD actual):**

```bash
# Desde tu máquina local
scp "E:\AmandaBoutique desarrollo\db.sqlite3" usuario@servidor:/var/www/amandaboutique/
```

**Si migras a PostgreSQL:**

```bash
# En desarrollo, exportar datos
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datadump.json

# Transferir al servidor
scp datadump.json usuario@servidor:/var/www/amandaboutique/

# En producción, importar datos (después de configurar settings.py)
python manage.py loaddata datadump.json
```

### 2.4 Transferir Archivos Media

```bash
# Desde tu máquina local
scp -r "E:\AmandaBoutique desarrollo\media" usuario@servidor:/var/www/amandaboutique/
```

---

## ⚙️ Fase 3: Configuración del Proyecto

### 3.1 Crear Entorno Virtual

```bash
cd /var/www/amandaboutique
python3 -m venv venv
source venv/bin/activate
```

### 3.2 Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Servidor WSGI para producción
```

**Si usas PostgreSQL, agregar:**

```bash
pip install psycopg2-binary
```

### 3.3 Configurar settings.py para Producción

Crear archivo `AmandaProjecto/settings_prod.py`:

```python
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com', 'IP_DEL_SERVIDOR']

# Database (si usas PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'amandaboutique',
        'USER': 'amandauser',
        'PASSWORD': 'tu_contraseña_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Si mantienes SQLite, comentar lo anterior y usar:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = ['https://tudominio.com', 'https://www.tudominio.com']
```

### 3.4 Configurar Variable de Entorno

```bash
# Editar .bashrc o crear archivo .env
echo 'export DJANGO_SETTINGS_MODULE=AmandaProjecto.settings_prod' >> ~/.bashrc
source ~/.bashrc
```

### 3.5 Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 3.6 Aplicar Migraciones (si es necesario)

```bash
python manage.py migrate
```

### 3.7 Crear Superusuario (si es nuevo servidor)

```bash
python manage.py createsuperuser
```

---

## 🔧 Fase 4: Configurar Gunicorn

### 4.1 Crear Archivo de Socket

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Contenido:

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### 4.2 Crear Servicio de Gunicorn

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Contenido:

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=TU_USUARIO
Group=www-data
WorkingDirectory=/var/www/amandaboutique
Environment="PATH=/var/www/amandaboutique/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=AmandaProjecto.settings_prod"
ExecStart=/var/www/amandaboutique/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          AmandaProjecto.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4.3 Iniciar y Habilitar Gunicorn

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

### 4.4 Verificar Socket

```bash
sudo systemctl status gunicorn
curl --unix-socket /run/gunicorn.sock localhost
```

---

## 🌐 Fase 5: Configurar Nginx

### 5.1 Crear Configuración del Sitio

```bash
sudo nano /etc/nginx/sites-available/amandaboutique
```

Contenido:

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/amandaboutique/staticfiles/;
    }

    location /media/ {
        alias /var/www/amandaboutique/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    client_max_body_size 10M;
}
```

### 5.2 Habilitar Sitio

```bash
sudo ln -s /etc/nginx/sites-available/amandaboutique /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5.3 Configurar Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 🔒 Fase 6: Configurar HTTPS con Let's Encrypt

### 6.1 Instalar Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 6.2 Obtener Certificado SSL

```bash
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

Seguir las instrucciones en pantalla.

### 6.3 Verificar Renovación Automática

```bash
sudo certbot renew --dry-run
```

---

## 💾 Fase 7: Configurar Backups Automáticos

### 7.1 Crear Script de Backup

```bash
sudo nano /usr/local/bin/backup_amandaboutique.sh
```

Contenido:

```bash
#!/bin/bash

# Configuración
BACKUP_DIR="/var/backups/amandaboutique"
PROJECT_DIR="/var/www/amandaboutique"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

# Backup de base de datos
if [ -f "$PROJECT_DIR/db.sqlite3" ]; then
    cp $PROJECT_DIR/db.sqlite3 $BACKUP_DIR/db_$DATE.sqlite3
fi

# Backup de archivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $PROJECT_DIR media/

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "db_*.sqlite3" -mtime +30 -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +30 -delete

echo "Backup completado: $DATE"
```

Dar permisos de ejecución:

```bash
sudo chmod +x /usr/local/bin/backup_amandaboutique.sh
```

### 7.2 Programar Backup Diario con Cron

```bash
sudo crontab -e
```

Agregar línea:

```cron
0 2 * * * /usr/local/bin/backup_amandaboutique.sh >> /var/log/amandaboutique_backup.log 2>&1
```

Esto ejecutará el backup todos los días a las 2:00 AM.

---

## 🧪 Fase 8: Pruebas y Verificación

### 8.1 Checklist de Verificación

- [ ] Sitio accesible vía HTTPS
- [ ] Login funciona correctamente
- [ ] Todos los módulos cargan sin errores
- [ ] Imágenes y archivos media se muestran correctamente
- [ ] Archivos estáticos (CSS, JS) cargan correctamente
- [ ] Formularios funcionan (crear, editar, eliminar)
- [ ] Exportación a PDF funciona
- [ ] Permisos de usuario funcionan correctamente
- [ ] Responsive design funciona en móvil
- [ ] Certificado SSL válido

### 8.2 Pruebas de Funcionalidad

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

## 🔄 Fase 9: Mantenimiento Continuo

### 9.1 Monitoreo de Logs

```bash
# Ver logs de Gunicorn
sudo journalctl -u gunicorn

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Ver logs de Django (si configurado)
tail -f /var/www/amandaboutique/logs/django.log
```

### 9.2 Actualizar el Proyecto

```bash
cd /var/www/amandaboutique
source venv/bin/activate

# Actualizar código
git pull origin main  # o transferir archivos manualmente

# Instalar nuevas dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Recolectar estáticos
python manage.py collectstatic --noinput

# Reiniciar Gunicorn
sudo systemctl restart gunicorn
```

### 9.3 Restaurar Backup

```bash
# Detener servicio
sudo systemctl stop gunicorn

# Restaurar base de datos
cp /var/backups/amandaboutique/db_FECHA.sqlite3 /var/www/amandaboutique/db.sqlite3

# Restaurar media
cd /var/www/amandaboutique
rm -rf media/
tar -xzf /var/backups/amandaboutique/media_FECHA.tar.gz

# Reiniciar servicio
sudo systemctl start gunicorn
```

---

## 📊 Fase 10: Optimizaciones Opcionales

### 10.1 Configurar Redis para Caché (Opcional)

```bash
sudo apt install redis-server -y
pip install django-redis
```

Agregar a `settings_prod.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 10.2 Configurar Monitoreo con Sentry (Opcional)

```bash
pip install sentry-sdk
```

Agregar a `settings_prod.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="TU_DSN_DE_SENTRY",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

---

## 🆘 Solución de Problemas Comunes

### Error 502 Bad Gateway

```bash
# Verificar estado de Gunicorn
sudo systemctl status gunicorn

# Reiniciar Gunicorn
sudo systemctl restart gunicorn

# Ver logs
sudo journalctl -u gunicorn -n 50
```

### Archivos Estáticos No Cargan

```bash
# Recolectar estáticos nuevamente
python manage.py collectstatic --noinput

# Verificar permisos
sudo chown -R www-data:www-data /var/www/amandaboutique/staticfiles/
```

### Error de Permisos en Media

```bash
sudo chown -R www-data:www-data /var/www/amandaboutique/media/
sudo chmod -R 755 /var/www/amandaboutique/media/
```

### Base de Datos Bloqueada (SQLite)

```bash
# Verificar procesos
sudo lsof /var/www/amandaboutique/db.sqlite3

# Reiniciar Gunicorn
sudo systemctl restart gunicorn
```

---

## 📞 Contacto y Soporte

Para soporte técnico o consultas sobre el despliegue:

- Revisar logs del sistema
- Consultar documentación de Django
- Contactar al desarrollador del sistema

---

## ✅ Checklist Final de Producción

- [ ] Servidor configurado y actualizado
- [ ] Proyecto desplegado en `/var/www/amandaboutique`
- [ ] Base de datos migrada y funcionando
- [ ] Archivos media transferidos
- [ ] Gunicorn configurado y corriendo
- [ ] Nginx configurado y corriendo
- [ ] HTTPS configurado con Let's Encrypt
- [ ] Backups automáticos configurados
- [ ] Todas las pruebas pasadas
- [ ] Monitoreo de logs configurado
- [ ] Documentación actualizada
- [ ] Usuarios informados del nuevo sistema

---

**Fecha de creación**: 21 de diciembre de 2025  
**Versión del plan**: 1.0  
**Proyecto**: Amanda Mateo Boutique v3.0
