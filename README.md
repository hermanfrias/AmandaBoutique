# Amanda Mateo Boutique - Sistema de Gestión

Sistema web completo para la gestión de boutique desarrollado con Django, que incluye gestión de inventario, citas, clientes, proveedores, flujo de caja y control de usuarios con permisos granulares.

## Características Principales

### 📦 Gestión de Catálogo

- CRUD completo de productos
- Búsqueda y filtrado de artículos
- Exportación a PDF (lista y tarjetas)
- Control de permisos por usuario

### 📅 Sistema de Citas

- Calendario interactivo para agendar citas
- Visualización mensual y semanal
- Estados de citas (Pendiente, Confirmada, Completada, Cancelada)
- Gestión completa de citas con permisos

### 👥 Gestión de Clientes

- Registro completo de clientes
- Historial de interacciones
- Búsqueda y filtrado
- Permisos de acceso configurables

### 🏢 Gestión de Proveedores

- Administración de proveedores
- Información de contacto y detalles
- Control de acceso por permisos

### 💰 Flujo de Caja

- Registro de movimientos (Ingresos/Egresos)
- Cotización del dólar
- Dashboard con resumen financiero
- Exportación a Excel y PDF
- Filtrado por fechas y tipos

### 🔐 Sistema de Permisos de Usuario

- **Registro con permisos de solo lectura por defecto**
- **Gestión de permisos por superusuarios**
- Permisos granulares por módulo:
  - Ver (view)
  - Agregar (add)
  - Cambiar (change)
  - Eliminar (delete)
- **Interfaz de gestión de usuarios**
- **Eliminación de usuarios (solo no-superusuarios)**
- Protección de vistas con decoradores
- UI adaptativa según permisos

## Tecnologías Utilizadas

- **Backend**: Django 5.1.4
- **Base de datos**: SQLite (desarrollo)
- **Frontend**: HTML5, CSS3, JavaScript
- **Estilos**: Bootstrap 5 + CSS personalizado
- **Exportación**: ReportLab (PDF), OpenPyXL (Excel)
- **Calendario**: FullCalendar.js

## Estructura del Proyecto

```
AmandaBoutique/
├── BoutiqueApp/          # Gestión de catálogo
├── citas/                # Sistema de citas
├── ClientesApp/          # Gestión de clientes
├── ProveedoresApp/       # Gestión de proveedores
├── flujo/                # Flujo de caja y cotizaciones
├── LoginApp/             # Autenticación y permisos
├── static/               # Archivos estáticos (CSS, JS, imágenes)
└── templates/            # Templates base
```

## Instalación

1. **Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd AmandaBoutique
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Aplicar migraciones**

```bash
python manage.py migrate
```

5. **Crear superusuario**

```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**

```bash
python manage.py runserver
```

7. **Acceder a la aplicación**

- URL: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Sistema de Permisos

### Configuración Inicial

- Los nuevos usuarios se registran con **permisos de solo lectura** (view) en todos los módulos
- Solo los **superusuarios** pueden modificar permisos de otros usuarios

### Gestión de Permisos

1. Acceder como superusuario
2. Ir a **Admin → Gestionar Usuarios**
3. Seleccionar usuario y hacer clic en **Editar Permisos**
4. Asignar permisos por módulo:
   - ✅ Ver - Solo lectura
   - ➕ Agregar - Crear nuevos registros
   - ✏️ Cambiar - Editar registros existentes
   - 🗑️ Eliminar - Borrar registros

### Módulos con Control de Permisos

- Catálogo
- Citas
- Clientes
- Proveedores
- Movimientos de Caja
- Cotización Dólar

## Guía de Uso

### Gestión de Catálogo

1. Navegar a **Catálogo**
2. Usar **Agregar** para nuevos productos (requiere permiso)
3. Buscar productos por nombre
4. Exportar a PDF (lista o tarjetas)
5. Editar/Eliminar productos (requiere permisos)

### Sistema de Citas

1. Ir a **Citas → Calendario**
2. Hacer clic en una fecha para crear cita (requiere permiso)
3. Ver todas las citas en **Listar Citas**
4. Cambiar estado de citas según progreso
5. Editar o eliminar citas (requiere permisos)

### Flujo de Caja

1. Acceder a **Flujo de Caja**
2. Registrar movimientos (Ingreso/Egreso)
3. Actualizar cotización del dólar
4. Ver dashboard con resumen
5. Exportar reportes a Excel o PDF
6. Filtrar por rango de fechas

### Gestión de Usuarios (Solo Superusuarios)

1. Ir a **Admin → Gestionar Usuarios**
2. Ver lista de todos los usuarios
3. **Editar Permisos**: Asignar/revocar permisos por módulo
4. **Eliminar**: Borrar usuarios (excepto superusuarios)

## Estándares de Diseño

### Botones Estandarizados

- **Guardar**: `btn-pink` (rosa) - Guardar cambios
- **Editar**: `btn-editar` (amarillo) - Modificar registros
- **Eliminar**: `btn-eliminar` (rojo) - Borrar registros
- **Ver**: `btn-ver` (azul) - Ver detalles
- **Agregar**: `btn-listar` (verde) - Crear nuevos
- **Volver**: `btn-volver` / `btn-secondary` (gris) - Regresar

### Paleta de Colores

- **Principal**: Rosa (#b76e79)
- **Fondo**: Rosa claro (#fff5fa)
- **Encabezados**: Rosa (#ffe6f2)
- **Texto**: Gris oscuro

## Seguridad

- ✅ Autenticación requerida para todas las vistas
- ✅ Permisos granulares por modelo y acción
- ✅ Protección CSRF en formularios
- ✅ Validación de permisos en backend
- ✅ UI adaptativa según permisos del usuario
- ✅ Superusuarios protegidos contra eliminación

## Funcionalidades Destacadas

### Exportación de Datos

- **PDF**: Catálogo (lista y tarjetas), Movimientos de caja
- **Excel**: Movimientos de caja con filtros

### Dashboard Financiero

- Resumen de ingresos y egresos
- Gráficos de movimientos
- Balance actual
- Cotización del dólar actualizada

### Interfaz Responsiva

- Diseño adaptable a diferentes dispositivos
- Navegación intuitiva
- Feedback visual en acciones

## Próximas Mejoras

- [ ] Reportes avanzados con gráficos
- [ ] Notificaciones de citas
- [ ] Historial de cambios por usuario
- [ ] Backup automático de base de datos
- [ ] API REST para integración

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto es privado y de uso exclusivo para Amanda Mateo Boutique.

## Soporte

Para soporte o consultas, contactar al administrador del sistema.

---

**Versión**: 2.0  
**Última actualización**: Diciembre 2025  
**Desarrollado con**: Django 5.1.4 + Bootstrap 5
