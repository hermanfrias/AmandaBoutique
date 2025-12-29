# Guía de Migración a Producción - Amanda Mateo Boutique

## Cambios Implementados (Diciembre 2025)

### Nuevas Funcionalidades

1. **Soporte para 4 Fotos**

   - Catálogo: `imagen_modelo` + `foto2`, `foto3`, `foto4`
   - Vestidos: `foto1`, `foto2`, `foto3`, `foto4`

2. **Presentación Mejorada**

   - Carousel con navegación en vistas de detalle
   - Modal lightbox con zoom para todas las fotos
   - Efectos hover y transiciones suaves

3. **Acceso Público**

   - Detalles de catálogo y vestidos visibles sin login
   - Enlaces clickeables desde la página principal
   - Historial de alquileres restringido a usuarios autorizados

4. **Gestión de Permisos Mejorada**
   - Permisos para todos los módulos nuevos
   - Configuración IVA, Insumos, Activos Fijos, Alquiler

---

## Paso a Paso: Migración a Producción

### 📋 Pre-requisitos

- Acceso SSH al servidor de producción
- Backup de la base de datos actual
- Backup de archivos media actuales

### 🔧 Paso 1: Preparación en Desarrollo

```powershell
# 1. Verificar que todos los cambios están commiteados
git status

# 2. Asegurarse de estar en la rama main
git checkout main

# 3. Verificar que todo funciona localmente
python manage.py check
python manage.py test
```

### 📦 Paso 2: Backup en Producción

```bash
# Conectar al servidor de producción
ssh usuario@servidor

# Navegar al directorio del proyecto
cd /ruta/al/proyecto

# Backup de la base de datos
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Backup de archivos media
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/

# Backup del código actual
git stash
```

### 🚀 Paso 3: Actualizar Código en Producción

```bash
# Actualizar desde el repositorio
git pull origin main

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar/actualizar dependencias
pip install -r requirements.txt
```

### 🗄️ Paso 4: Aplicar Migraciones de Base de Datos

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Aplicar migraciones
python manage.py migrate BoutiqueApp
python manage.py migrate Alquiler

# Verificar que se aplicaron correctamente
python manage.py showmigrations
```

**Migraciones a aplicar:**

- `BoutiqueApp.0004_catalogo_foto2_catalogo_foto3_catalogo_foto4_and_more`
- `Alquiler.0007_vestido_foto3_vestido_foto4`

### 📁 Paso 5: Recolectar Archivos Estáticos

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Verificar que se copiaron los nuevos CSS
ls staticfiles/alquiler/css/catalogo_pdf.css
ls staticfiles/BoutiqueApp/css/catalog_cards.css
```

### 🔐 Paso 6: Verificar Permisos (Opcional)

Si usas usuarios con permisos específicos:

```bash
# Acceder al shell de Django
python manage.py shell

# Verificar que los nuevos permisos existen
from django.contrib.auth.models import Permission
Permission.objects.filter(content_type__app_label='Alquiler').count()
Permission.objects.filter(content_type__app_label='Inventario').count()
```

### 🔄 Paso 7: Reiniciar Servicios

**Para NSSM (Windows Server):**

```powershell
# Detener el servicio
nssm stop DjangoServidor

# Iniciar el servicio
nssm start DjangoServidor

# Verificar estado
nssm status DjangoServidor
```

**Para Gunicorn/Nginx (Linux):**

```bash
# Reiniciar Gunicorn
sudo systemctl restart gunicorn

# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar estado
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### ✅ Paso 8: Verificación Post-Migración

1. **Verificar acceso al sitio:**

   - Abrir navegador y acceder a la URL de producción
   - Verificar que carga correctamente

2. **Probar funcionalidades nuevas:**

   - [ ] Acceder a la página principal sin login
   - [ ] Hacer clic en una tarjeta del showroom
   - [ ] Verificar que se ve el carousel de fotos
   - [ ] Hacer clic en una foto para ver el zoom
   - [ ] Navegar entre fotos en el modal
   - [ ] Probar con vestidos de alquiler

3. **Verificar permisos:**

   - [ ] Iniciar sesión como administrador
   - [ ] Ir a Gestionar Permisos
   - [ ] Verificar que aparecen todos los módulos nuevos
   - [ ] Editar permisos de un usuario de prueba

4. **Verificar formularios:**
   - [ ] Crear/editar un catálogo con 4 fotos
   - [ ] Crear/editar un vestido con 4 fotos
   - [ ] Verificar que las fotos se guardan correctamente

### 🔍 Paso 9: Monitoreo

```bash
# Ver logs en tiempo real
tail -f /var/log/gunicorn/error.log  # Linux
# o revisar logs de NSSM en Windows

# Verificar uso de recursos
htop  # Linux
# o Task Manager en Windows
```

### 🆘 Paso 10: Rollback (Si es necesario)

Si algo sale mal:

```bash
# Revertir código
git reset --hard HEAD~1

# Restaurar base de datos
python manage.py loaddata backup_YYYYMMDD_HHMMSS.json

# Restaurar media
tar -xzf media_backup_YYYYMMDD_HHMMSS.tar.gz

# Reiniciar servicios
# (usar comandos del Paso 7)
```

---

## 📝 Checklist de Migración

### Antes de Migrar

- [ ] Código commiteado y pusheado
- [ ] Tests pasando en desarrollo
- [ ] Backup de base de datos creado
- [ ] Backup de archivos media creado
- [ ] Notificar a usuarios sobre mantenimiento (si aplica)

### Durante la Migración

- [ ] Código actualizado en producción
- [ ] Migraciones aplicadas correctamente
- [ ] Archivos estáticos recolectados
- [ ] Servicios reiniciados

### Después de Migrar

- [ ] Sitio accesible
- [ ] Funcionalidades nuevas probadas
- [ ] Logs revisados sin errores
- [ ] Usuarios notificados de nueva versión

---

## 🐛 Solución de Problemas Comunes

### Error: "No such table" o "column does not exist"

**Solución:** Las migraciones no se aplicaron correctamente

```bash
python manage.py migrate --run-syncdb
```

### Error: "Static file not found"

**Solución:** Archivos estáticos no recolectados

```bash
python manage.py collectstatic --clear --noinput
```

### Error: "Permission denied" al subir fotos

**Solución:** Permisos de carpeta media incorrectos

```bash
chmod -R 755 media/
chown -R www-data:www-data media/  # Linux
```

### Las fotos antiguas no se ven

**Solución:** Campo renombrado, verificar que `imagen_modelo` existe

- En BoutiqueApp se mantuvo `imagen_modelo` (no se renombró)
- En Alquiler se usa `foto1`, `foto2`, `foto3`, `foto4`

---

## 📞 Contacto y Soporte

Si encuentras problemas durante la migración:

1. Revisar logs del servidor
2. Verificar que todas las migraciones se aplicaron
3. Confirmar que los archivos estáticos se recolectaron
4. Revisar permisos de archivos y carpetas

**Recuerda:** Siempre tener backups antes de cualquier migración a producción.
