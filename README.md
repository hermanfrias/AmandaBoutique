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

- **Registro completo de movimientos financieros**
  - Ingresos y Gastos
  - Tipo de movimiento: Venta, Compra de Insumos, Nómina, Alquiler, Otros
  - Método de pago: Efectivo, Depósito, Transferencia, Pago Móvil, Otro
  - Moneda: Bolívares o Dólares
- **CRUD completo de movimientos**
  - Crear, editar y eliminar movimientos
  - Confirmación modal antes de eliminar
  - Fecha pre-cargada en formulario de edición
- **Cotización del dólar**
  - Registro diario de cotización
  - Conversión automática Bs → USD
  - Validación de cotización al crear movimientos en Bs
- **Dashboard financiero interactivo**
  - Resumen mensual, anual y total
  - Gráficos de ingresos y gastos
  - Rentabilidad calculada
- **Filtros avanzados**
  - Por rango de fechas
  - Por tipo (Ingreso/Gasto)
  - Por tipo de movimiento
  - Por método de pago
  - Por moneda
- **Exportación profesional**
  - Excel con todas las columnas
  - PDF con formato optimizado
  - Filtros aplicables a exportaciones
- **Interfaz optimizada**
  - Tabla responsiva con columnas ajustables
  - Botones de acción claros y accesibles
  - Descripción con ajuste de texto multilínea

### 📦 Gestión de Inventario

- **Control de Existencias de Insumos**
  - Registro de insumos con código auto-generado (INS0001, INS0002...)
  - Descripción, unidad de medida (Unidades/Metros)
  - **Categorías de insumos** - Clasificación por tipo (Telas, Hilos, Botones, etc.)
  - **Proveedores** - Asignación de proveedor a cada insumo
  - Existencia actual y existencia mínima
  - Costo unitario en USD (calculado automáticamente)
  - Fecha de creación
  - **Filtros avanzados** - Por categoría y proveedor en listado
- **Compras de Insumos**
  - **Agrupación por factura** - Compras organizadas por número de factura y fecha
  - **Creación de múltiples ítems** - Formset para agregar varios insumos en una factura
  - Registro de compras con número de factura opcional
  - **Selector de insumos con búsqueda** - Integración con Select2 para búsqueda rápida
  - Cantidad y moneda (Bolívares o Dólares)
  - Opción de aplicar IVA (16%)
  - Conversión automática de moneda usando cotización del día
  - Cálculo automático de totales con/sin IVA
  - **Actualización automática**: Al registrar una compra:
    - Se suma la cantidad al inventario
    - Se calcula el costo unitario: `monto_total_usd / cantidad`
    - **Se crea automáticamente un MovimientoCaja** en el módulo de flujo
  - **Gestión de grupos de compras**:
    - Ver detalle completo de factura con todos sus ítems
    - Editar cantidades y montos de ítems individuales
    - Eliminar ítems individuales de una factura
    - Eliminar factura completa con confirmación
  - **Corrección de bug**: Editar compra ahora ajusta correctamente el inventario
- **Uso de Insumos**
  - Registro de consumo de insumos con descripción
  - Formulario dinámico para agregar múltiples insumos
  - **Actualización automática**: Al registrar un uso:
    - Se resta la cantidad del inventario
    - Se calcula el costo total del uso
  - Validación de existencia suficiente
  - Restauración automática de stock al eliminar un uso
- **Reportes y Seguimiento**
  - Historial de compras por insumo
  - Historial de usos por insumo
  - Cálculo de costos de producción
  - Alertas de stock mínimo (visual)
  - **Exportación a PDF** - Reporte completo de inventario con valor total
  - **Cálculo correcto de valor total** - Suma de (existencia × costo unitario)
- **Integración con Flujo de Caja**
  - **Creación automática de movimientos** - Cada compra genera un MovimientoCaja
  - **Actualización automática** - Al editar compra, se actualiza el movimiento
  - Descripción: "Compra insumos varios"
  - Tipo: "Gasto"
  - Método de pago: "Efectivo"

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
├── Inventario/           # Gestión de inventario de insumos
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

#### Gestión de Movimientos

1. Acceder a **Flujo de Caja → Movimientos**
2. **Crear nuevo movimiento** (requiere permiso):
   - Seleccionar fecha
   - Ingresar descripción
   - Elegir tipo: Ingreso o Gasto
   - Seleccionar moneda: Bolívares ($) o Dólares (Bs)
   - Ingresar monto
   - **Opcional**: Tipo de movimiento (Venta, Compra de Insumos, Nómina, Alquiler, Otros)
   - **Opcional**: Método de pago (Efectivo, Depósito, Transferencia, Pago Móvil, Otro)
3. **Editar movimiento** (requiere permiso):
   - Clic en botón "Editar"
   - Modificar campos necesarios (fecha pre-cargada)
   - Guardar cambios
4. **Eliminar movimiento** (requiere permiso):
   - Clic en botón "Eliminar"
   - Confirmar en modal de seguridad

#### Filtros Avanzados

Usar la sección de filtros para buscar movimientos específicos:

- **Fecha Inicio/Fin**: Rango de fechas
- **Tipo**: Ingreso o Gasto
- **Tipo Mov.**: Venta, Compra de Insumos, Nómina, Alquiler, Otros
- **Método Pago**: Efectivo, Depósito, Transferencia, Pago Móvil, Otro
- **Moneda**: Bolívares o Dólares

Los filtros se pueden combinar para búsquedas precisas.

#### Cotización del Dólar

1. Ir a **Flujo de Caja → Cotizaciones**
2. Registrar cotización diaria (requiere permiso)
3. **Importante**: Debe existir cotización para la fecha antes de crear movimientos en Bolívares

#### Dashboard y Reportes

1. Ver **Dashboard** para resumen visual:
   - Totales mensuales, anuales y acumulados
   - Gráficos de ingresos vs gastos
   - Rentabilidad calculada
2. **Exportar a Excel**:
   - Clic en "Exportar"
   - Seleccionar rango de fechas (opcional)
   - Descargar archivo con todas las columnas
3. **Exportar a PDF**:
   - Clic en "Exportar"
   - Seleccionar rango de fechas (opcional)
   - Imprimir o guardar PDF formateado

### Gestión de Inventario

#### Insumos

1. Acceder a **Admin → Insumos**
2. **Crear nuevo insumo**:
   - El código se genera automáticamente (INS0001, INS0002...)
   - Ingresar descripción
   - Seleccionar unidad de medida (Unidades o Metros)
   - Ingresar existencia inicial
   - Definir existencia mínima (para alertas)
   - **Opcional**: Ingresar costo unitario (o dejarlo vacío para cálculo automático)
3. **Ver detalle**: Muestra historial de compras y usos

#### Compras de Insumos

1. Ir a **Admin → Compras de Insumos**
2. **Registrar compra**:
   - Seleccionar insumo
   - Ingresar fecha de compra
   - Ingresar cantidad comprada
   - Seleccionar moneda (Bs o $)
   - Ingresar monto
   - Marcar si aplica IVA (16%)
3. **Actualización automática**:
   - Se suma la cantidad al inventario
   - Se calcula el costo unitario: `monto_total_usd / cantidad`
   - Se convierten montos según cotización del día

#### Uso de Insumos

1. Ir a **Admin → Uso de Insumos**
2. **Registrar uso**:
   - Ingresar fecha de uso
   - Describir el uso (ej: "Vestido para cliente María")
   - Agregar insumos utilizados:
     - Seleccionar insumo (muestra existencia disponible)
     - Ingresar cantidad utilizada
     - Usar botón "+ Agregar Insumo" para más insumos
3. **Validaciones automáticas**:
   - Verifica existencia suficiente
   - Valida que el insumo tenga costo definido
4. **Actualización automática**:
   - Se resta la cantidad del inventario
   - Se calcula el costo total del uso
5. **Editar/Eliminar**:
   - Al editar: ajusta inventario según diferencia
   - Al eliminar: restaura existencias automáticamente

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

**Versión**: 2.4  
**Última actualización**: 16 de diciembre de 2024 - Compras Agrupadas y Movimientos Automáticos  
**Desarrollado con**: Django 5.1.4 + Bootstrap 5
