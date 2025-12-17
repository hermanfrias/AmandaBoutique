# Revisión del Proyecto Amanda Boutique en Producción

**Fecha de Creación:** 28 de noviembre de 2025  
**Última Actualización:** 17 de diciembre de 2025  
**Servidor:** 192.168.1.193:8000 (Producción) / 192.168.1.193:9000 (AsoTunapuy)  
**Servicio:** DjangoServidor (NSSM)

---

## ✅ Estado del Servicio

### Configuración NSSM

- **Estado:** `SERVICE_RUNNING` ✓
- **Nombre del Servicio:** DjangoServidor
- **Ejecutable:** `E:\AmandaBoutique\.venv\Scripts\python.exe`
- **Directorio de Trabajo:** `E:\AmandaBoutique`
- **Script:** `server.py` (usando Waitress)
- **IP/Puerto:** 192.168.1.193:8000

El servicio está corriendo correctamente y configurado para usar Waitress como servidor WSGI de producción.

---

## 📋 Cambios Recientes Implementados (Nov 28 - Dic 15, 2025)

### 🎨 Estandarización de UI y Diseño (Dic 6-14)

#### 1. **Estandarización de Botones en Todo el Proyecto** ✅

**Objetivo:** Crear una experiencia de usuario consistente en todos los módulos.

**Cambios implementados:**

- ✅ **Eliminación de todos los iconos de botones** - Interfaz más limpia y moderna
- ✅ **Colores estandarizados:**
  - `btn-pink` - Guardar cambios (rosa)
  - `btn-editar` - Editar registros (amarillo)
  - `btn-eliminar` - Eliminar registros (rojo)
  - `btn-ver` - Ver detalles (azul suave/rosa suave)
  - `btn-listar` - Agregar nuevos (verde)
  - `btn-volver` / `btn-secondary` - Volver/Cancelar (gris)
- ✅ **Tamaño consistente:** Uso de `btn-sm` en todos los botones de acción
- ✅ **Cambio de terminología:** "Cancelar" → "Volver" en todos los formularios
- ✅ **Centrado de botones:** Botones de formulario agrupados y centrados

**Módulos actualizados:**

- BoutiqueApp (Catálogo)
- ClientesApp
- ProveedoresApp
- citas
- flujo (Flujo de Caja)
- Inventario
- LoginApp

#### 2. **Estandarización de Templates** ✅

- ✅ **Formato consistente de Django template tags** - Cada tag en su propia línea
- ✅ **Corrección de títulos de página** - Títulos correctos en todas las vistas
- ✅ **Herencia correcta:** Todos los templates extienden de `BoutiqueApp/base.html`
- ✅ **Eliminación de estilos inline** - Migrados a `estilos.css`
- ✅ **Estructura de tablas estandarizada** - Diseño consistente en todas las listas
- ✅ **Normalización de line endings** - Consistencia en archivos de texto

**Archivos corregidos:**

- Renombrado: `LoginApp/froms.py` → `LoginApp/forms.py`
- Templates de todos los módulos formateados
- CSS centralizado en archivos externos

### 💰 Mejoras del Módulo Flujo de Caja (Nov 28 - Dic 9)

#### 1. **Gestión de Cotizaciones del Dólar** ✅

- ✅ **CRUD completo de cotizaciones**
  - Crear cotización diaria
  - Listar cotizaciones con historial
  - Editar cotizaciones existentes
  - Eliminar cotizaciones
- ✅ **Validación automática** - Requiere cotización para movimientos en Bs
- ✅ **Conversión automática** - Bs → USD usando cotización del día

**Archivos modificados:**

- [`flujo/views.py`](file:///E:/AmandaBoutique/flujo/views.py) - Vistas de CRUD
- [`flujo/templates/flujo/listar_cotizaciones.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/listar_cotizaciones.html)
- [`flujo/templates/flujo/editar_cotizacion.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/editar_cotizacion.html)

#### 2. **Dashboard Financiero Mejorado** ✅

**Nuevas funcionalidades:**

- ✅ **Métricas de rentabilidad** - Cálculo: `(Saldo / Ingresos) × 100`
- ✅ **Contadores de transacciones** - Cantidad de ingresos y gastos
- ✅ **Filtros avanzados** - Por mes y año específico
- ✅ **Conversión a Bolívares** - Totales estimados en Bs
- ✅ **Gráfico anual interactivo** - Chart.js con comportamiento mensual
- ✅ **Manejo robusto de errores** - Try/catch con traceback detallado

**Métricas mostradas:**

```
USD:
- Total Ingresos USD + cantidad de transacciones
- Total Gastos USD + cantidad de transacciones
- Saldo USD
- Rentabilidad (%) con indicador visual

Bolívares (Estimado):
- Total Ingresos Bs
- Total Gastos Bs
- Saldo Bs
```

#### 3. **Mejoras en Gestión de Movimientos** ✅

- ✅ **CRUD completo:** Crear, editar, eliminar movimientos
- ✅ **Modal de confirmación** - Antes de eliminar
- ✅ **Fecha pre-cargada** - En formulario de edición
- ✅ **Campos opcionales mejorados:**
  - Tipo de movimiento (Venta, Compra de Insumos, Nómina, Alquiler, Otros)
  - Método de pago (Efectivo, Depósito, Transferencia, Pago Móvil, Otro)

#### 4. **Filtros y Exportación** ✅

**Filtros avanzados:**

- Por rango de fechas (Inicio/Fin)
- Por tipo (Ingreso/Gasto)
- Por tipo de movimiento
- Por método de pago
- Por moneda (Bs/$)

**Exportación mejorada:**

- ✅ **PDF optimizado** - Formato profesional con filtros aplicados
- ✅ **Excel completo** - Todas las columnas con filtros
- ✅ **Filtros en reportes** - Los filtros se reflejan en exportaciones

#### 5. **Interfaz Optimizada** ✅

- ✅ **Tabla responsiva** - Columnas ajustables
- ✅ **Alineación correcta** - Montos alineados a la derecha
- ✅ **Descripción multilínea** - Ajuste de texto en celdas
- ✅ **Botones de acción claros** - Accesibles y visibles

### 📦 Módulo de Inventario de Insumos (Dic 2024)

#### **Sistema Completo de Gestión de Inventario** ✅

**Características principales:**

- ✅ **Control de Existencias:**

  - Código auto-generado (INS0001, INS0002...)
  - Descripción y unidad de medida (Unidades/Metros)
  - Existencia actual y mínima
  - Costo unitario en USD (calculado automáticamente)
  - Alertas visuales de stock mínimo

- ✅ **Compras de Insumos:**

  - Registro con fecha y cantidad
  - Moneda dual (Bs/$) con conversión automática
  - Opción de IVA (16%)
  - Actualización automática de inventario
  - Cálculo de costo unitario: `monto_total_usd / cantidad`

- ✅ **Uso de Insumos:**

  - Formulario dinámico para múltiples insumos
  - Validación de existencia suficiente
  - Actualización automática de stock
  - Cálculo de costos de producción
  - Restauración automática al eliminar

- ✅ **Reportes y Seguimiento:**
  - Historial de compras por insumo
  - Historial de usos por insumo
  - Cálculo de costos de producción

#### **Mejoras del Módulo de Inventario (Dic 15, 2025)** ✅

**Objetivo:** Mejorar la funcionalidad, usabilidad y precisión del módulo de inventario.

**Cambios implementados:**

1. **Nuevos Campos en Modelo Insumo** ✅

   - ✅ **Campo `proveedor`** - Relación ForeignKey con ProveedoresApp
   - ✅ **Campo `categoria`** - Clasificación de insumos (Telas, Hilos, Botones, Cierres, Elásticos, Adornos, Otros)
   - ✅ Migración de base de datos aplicada correctamente

2. **Filtros Avanzados en Listado de Insumos** ✅

   - ✅ **Filtro por Categoría** - Dropdown con todas las categorías disponibles
   - ✅ **Filtro por Proveedor** - Dropdown con todos los proveedores
   - ✅ Filtros aplicados correctamente en la vista `listar_insumos`
   - ✅ Interfaz de usuario mejorada con filtros visibles

3. **Integración de Select2 en Compras** ✅

   - ✅ **Selector de insumos con búsqueda** - Implementado en `form_compra.html`
   - ✅ **jQuery actualizado** - Versión 3.6.0 cargada correctamente
   - ✅ **Select2 configurado** - Búsqueda rápida de insumos por nombre
   - ✅ Mejora significativa en UX al registrar compras

4. **Corrección de Bug en Edición de Compras** ✅

   - ✅ **Problema identificado:** Al editar una compra, se sumaba incorrectamente al inventario
   - ✅ **Solución implementada:** Método `save()` en `CompraInsumo` ajustado
   - ✅ **Lógica correcta:**
     - Al crear: suma cantidad al inventario
     - Al editar: calcula diferencia y ajusta inventario
     - Al eliminar: resta cantidad del inventario
   - ✅ Validación de existencia suficiente al editar

5. **Actualización de Templates** ✅

   - ✅ **`form_insumo.html`** - Campos proveedor y categoría agregados
   - ✅ **`detalle_insumo.html`** - Muestra proveedor y categoría
   - ✅ **`listar_insumos.html`** - Botones de acción en una sola línea
   - ✅ **`insumos_pdf.html`** - Incluye proveedor y categoría en reporte

6. **Corrección de Cálculo en PDF de Inventario** ✅

   - ✅ **Problema:** Valor total del inventario calculado incorrectamente
   - ✅ **Solución:** Corregida lógica en `Inventario/views.py`
   - ✅ **Cálculo correcto:** `valor_total += insumo.existencia * insumo.costo_unitario`
   - ✅ Reporte PDF ahora muestra valores precisos

7. **Estandarización de Botones en Inventario** ✅

   - ✅ **Colores consistentes** - Alineados con el resto del proyecto
   - ✅ **Botón "Ver"** - Cambiado de `btn-info` a `btn-ver` (rosa suave)
   - ✅ **Botones centrados** - En formularios de guardar/volver
   - ✅ **Tamaño uniforme** - Uso de `btn-sm` en todos los botones

8. **Mensaje de Confirmación al Guardar** ✅
   - ✅ **Feedback visual** - Mensaje "Movimiento guardado correctamente"
   - ✅ Mejora en experiencia de usuario

**Archivos modificados:**

- [`Inventario/models.py`](file:///E:/AmandaBoutique/Inventario/models.py) - Nuevos campos y lógica de compras
- [`Inventario/views.py`](file:///E:/AmandaBoutique/Inventario/views.py) - Filtros y corrección de PDF
- [`Inventario/forms.py`](file:///E:/AmandaBoutique/Inventario/forms.py) - Campos actualizados
- [`Inventario/templates/Inventario/listar_insumos.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_insumos.html) - Filtros y botones
- [`Inventario/templates/Inventario/form_insumo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/form_insumo.html) - Nuevos campos
- [`Inventario/templates/Inventario/detalle_insumo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/detalle_insumo.html) - Visualización mejorada
- [`Inventario/templates/Inventario/form_compra.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/form_compra.html) - Select2 integrado
- [`Inventario/templates/Inventario/insumos_pdf.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/insumos_pdf.html) - Reporte mejorado

**Impacto:**

- ✅ **Mejor organización** - Categorías y proveedores facilitan la gestión
- ✅ **Búsqueda más rápida** - Select2 mejora significativamente la UX
- ✅ **Datos precisos** - Bug de edición corregido, inventario confiable
- ✅ **Reportes exactos** - PDF con cálculos correctos
- ✅ **UI consistente** - Botones estandarizados en todo el módulo

#### **Compras Agrupadas por Factura (Dic 16, 2025)** ✅

**Objetivo:** Refactorizar el módulo de compras para agrupar ítems por número de factura, permitiendo gestión de facturas completas.

**Cambios implementados:**

1. **Agrupación de Compras** ✅

   - ✅ **Vista de lista agrupada** - Compras organizadas por `numero_factura` + `fecha_compra`
   - ✅ **Cálculo de totales por grupo** - Subtotales, IVA y totales agregados
   - ✅ **Contador de ítems** - Muestra cantidad de ítems por factura
   - ✅ **Filtros y búsqueda** - Por rango de fechas y número de factura

2. **Nuevas Vistas de Grupo** ✅

   - ✅ **`detalle_compra_grupo`** - Muestra todos los ítems de una factura
   - ✅ **`editar_compra_grupo`** - Edita múltiples ítems con formset
   - ✅ **`eliminar_compra_grupo`** - Elimina factura completa con confirmación

3. **Nuevos Templates** ✅

   - ✅ **`detalle_compra_grupo.html`** - Detalle completo de factura
   - ✅ **`editar_compra_grupo.html`** - Formulario de edición con formset
   - ✅ **`eliminar_compra_grupo.html`** - Confirmación de eliminación

4. **Funcionalidad de Edición Mejorada** ✅

   - ✅ **Editar cantidades y montos** - Por ítem individual
   - ✅ **Eliminar ítems individuales** - Checkbox de eliminación en formset
   - ✅ **Validación de formset** - Manejo de errores mejorado
   - ✅ **Actualización de inventario** - Ajuste automático al editar/eliminar

5. **Limpieza de Código** ✅

   - ✅ **Templates eliminados** - 3 templates obsoletos removidos:
     - `detalle_compra.html` (reemplazado por `detalle_compra_grupo.html`)
     - `form_compra_editar.html` (reemplazado por `editar_compra_grupo.html`)
     - `eliminar_compra.html` (reemplazado por `eliminar_compra_grupo.html`)
   - ✅ **Vistas mantenidas** - Vistas antiguas conservadas para Django Admin

6. **Campo Editable en Admin** ✅

   - ✅ **`numero_factura` en CompraInsumoAdmin** - Ahora editable desde el admin de Django

**Archivos creados:**

- [`Inventario/views_grupo_compras.py`](file:///E:/AmandaBoutique/Inventario/views_grupo_compras.py) - Vistas de grupo
- [`Inventario/templates/Inventario/detalle_compra_grupo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/detalle_compra_grupo.html)
- [`Inventario/templates/Inventario/editar_compra_grupo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/editar_compra_grupo.html)
- [`Inventario/templates/Inventario/eliminar_compra_grupo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/eliminar_compra_grupo.html)

**Archivos modificados:**

- [`Inventario/views.py`](file:///E:/AmandaBoutique/Inventario/views.py) - Imports de vistas de grupo
- [`Inventario/admin.py`](file:///E:/AmandaBoutique/Inventario/admin.py) - Campo `numero_factura` editable
- [`Inventario/templates/Inventario/listar_compras.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_compras.html) - Vista agrupada

**Archivos eliminados:**

- `Inventario/templates/Inventario/detalle_compra.html`
- `Inventario/templates/Inventario/form_compra_editar.html`
- `Inventario/templates/Inventario/eliminar_compra.html`

#### **Movimientos de Caja Automáticos (Dic 16, 2025)** ✅

**Objetivo:** Crear automáticamente registros en `MovimientoCaja` al guardar compras de insumos.

**Implementación:**

1. **Django Signal** ✅

   - ✅ **Archivo creado:** [`Inventario/signals.py`](file:///E:/AmandaBoutique/Inventario/signals.py)
   - ✅ **Signal `post_save`** - Se ejecuta al guardar `CompraInsumo`
   - ✅ **Función:** `crear_o_actualizar_movimiento_caja`

2. **Comportamiento** ✅

   - ✅ **Compra nueva** - Crea `MovimientoCaja` con:
     - Descripción: "Compra insumos varios"
     - Tipo: "Gasto"
     - Tipo de movimiento: "Compra de Insumos"
     - Método de pago: "Efectivo"
     - Moneda: La misma de la compra (Bs o $)
     - Monto: Total con IVA de la compra
     - Fecha: Fecha de la compra
   - ✅ **Compra editada** - Actualiza el movimiento existente con nuevo monto

3. **Registro de Signals** ✅

   - ✅ **Archivo modificado:** [`Inventario/apps.py`](file:///E:/AmandaBoutique/Inventario/apps.py)
   - ✅ **Método `ready()`** - Importa signals al iniciar la app

**Impacto:**

- ✅ **Automatización completa** - No requiere intervención manual
- ✅ **Sincronización** - Inventario y flujo de caja siempre sincronizados
- ✅ **Trazabilidad** - Cada compra tiene su movimiento correspondiente
- ✅ **Actualización dinámica** - Cambios en compras se reflejan en movimientos

#### **Mejoras en Formateo de Código HTML (Dic 17, 2025)** ✅

**Objetivo:** Mejorar la legibilidad y mantenibilidad del código HTML en todos los templates de Django, aplicando estándares consistentes de formateo.

**Cambios implementados:**

1. **Indentación Consistente** ✅

   - ✅ **Espaciado uniforme** - 2 espacios por nivel de indentación
   - ✅ **Jerarquía visual clara** - Elementos anidados correctamente indentados
   - ✅ **Bloques Django** - Tags de template con indentación apropiada
   - ✅ Mejora significativa en legibilidad del código

2. **Espaciado de Django Template Tags** ✅

   - ✅ **Espacios alrededor de variables** - `{{ variable }}` en lugar de `{{variable}}`
   - ✅ **Espacios en tags de bloque** - `{% if condition %}` con espaciado correcto
   - ✅ **Consistencia** - Mismo estilo en todos los templates
   - ✅ Facilita lectura y debugging

3. **Limpieza de Código** ✅

   - ✅ **Eliminación de líneas en blanco excesivas** - Máximo 1-2 líneas entre secciones
   - ✅ **Comentarios HTML** - Bien formateados y útiles
   - ✅ **Atributos HTML** - Ordenados lógicamente
   - ✅ Código más limpio y profesional

4. **Templates Actualizados** ✅

   - ✅ **`compras_pdf.html`** - Formateo completo aplicado
   - ✅ **`form_compra.html`** - Indentación y espaciado mejorados
   - ✅ **`listar_insumos.html`** - Estructura clarificada
   - ✅ **`detalle_uso.html`** - Código reorganizado
   - ✅ Todos los templates del módulo Inventario revisados

**Beneficios:**

- ✅ **Mantenibilidad mejorada** - Código más fácil de leer y modificar
- ✅ **Prevención de errores** - Estructura clara reduce bugs
- ✅ **Colaboración facilitada** - Estándares consistentes para todo el equipo
- ✅ **Debugging más rápido** - Problemas más fáciles de identificar

**Archivos modificados:**

- [`Inventario/templates/Inventario/compras_pdf.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/compras_pdf.html)
- [`Inventario/templates/Inventario/form_compra.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/form_compra.html)
- [`Inventario/templates/Inventario/listar_insumos.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_insumos.html)
- [`Inventario/templates/Inventario/detalle_uso.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/detalle_uso.html)

**Estándares aplicados:**

```html
<!-- ANTES -->
<div class="container">
  <h1>{{titulo}}</h1>
  {% if condicion %}
  <p>Texto</p>
  {% endif %}
</div>

<!-- DESPUÉS -->
<div class="container">
  <h1>{{ titulo }}</h1>
  {% if condicion %}
  <p>Texto</p>
  {% endif %}
</div>
```

**Impacto:**

- ✅ **Calidad de código** - Estándares profesionales aplicados
- ✅ **Productividad** - Desarrollo más rápido con código limpio
- ✅ **Escalabilidad** - Base sólida para futuras mejoras
- ✅ **Profesionalismo** - Código que refleja buenas prácticas

---

#### **Sistema de Anulación de Compras (Dic 17, 2025)** ✅

**Objetivo:** Implementar sistema de anulación que reemplace la eliminación de compras, manteniendo trazabilidad completa y creando movimientos de reversa automáticos.

**Cambios implementados:**

1. **Modelo CompraInsumo Actualizado** ✅

   - ✅ **Campo `anulada`** - Boolean para marcar compras anuladas
   - ✅ **Campo `fecha_anulacion`** - DateTime para registro de cuándo se anuló
   - ✅ **Método `anular()`** - Maneja todo el proceso de anulación:
     - Marca como anulada
     - Revierte inventario automáticamente
     - Dispara signal para crear movimiento de reversa
   - ✅ **Migración:** `0004_comprainsumo_anulada_comprainsumo_fecha_anulacion.py`

2. **Modelo MovimientoCaja Actualizado** ✅

   - ✅ **Campo `numero_factura`** - Vinculación directa con facturas
   - ✅ Permite búsquedas precisas y creación de reversas
   - ✅ **Migración:** `0003_movimientocaja_numero_factura.py`

3. **Signals Mejorados** ✅

   - ✅ **`pre_save` signal** - Captura estado anterior de `anulada`
   - ✅ **`post_save` signal actualizado** - Detecta anulaciones y crea reversas
   - ✅ **Lógica de detección robusta:**
     - Compara estado anterior vs actual
     - Si cambió de `False` a `True` → Crea movimiento de reversa
     - Evita duplicados verificando estado previo
   - ✅ **Movimiento de reversa:**
     - Tipo: "Ingreso" (compensa el gasto original)
     - Descripción: "REVERSA - Anulación Factura [NÚMERO]"
     - Mismo monto que la compra original
     - Mismo número de factura para vinculación

4. **Vistas Actualizadas** ✅

   - ✅ **`anular_compra`** - Anula compra individual
   - ✅ **`anular_compra_grupo`** - Anula factura completa
   - ✅ Reemplazan vistas de eliminación
   - ✅ Confirmación antes de anular
   - ✅ Mensajes informativos al usuario

5. **Templates Nuevos** ✅

   - ✅ **`anular_compra.html`** - Confirmación de anulación individual
   - ✅ **`anular_compra_grupo.html`** - Confirmación de anulación de factura
   - ✅ Muestran advertencias y detalles antes de anular

6. **Templates Actualizados** ✅

   - ✅ **`listar_compras.html`** - Indicadores visuales:
     - Badge rojo "ANULADA" para compras anuladas
     - Fila tachada con opacidad reducida
     - Botones Editar/Anular ocultos para compras anuladas
     - Solo muestra botón "Ver" para compras anuladas
   - ✅ **`detalle_compra_grupo.html`** - Botón "Anular" agregado
   - ✅ **`listar_movimientos.html`** - Indicadores de reversa:
     - Badge amarillo "REVERSA" para movimientos de reversa
     - Fondo amarillo claro (#fff3cd) en filas de reversa
     - Fácil identificación visual

7. **URLs Actualizadas** ✅

   - ✅ Rutas de eliminación reemplazadas por rutas de anulación
   - ✅ `anular_compra/<int:pk>/`
   - ✅ `anular_compra_grupo/<str:numero_factura>/<str:fecha>/`

8. **Admin de Django Configurado** ✅

   - ✅ **Permisos de eliminación** - Solo superusuarios pueden eliminar
   - ✅ **Acción personalizada** - "Anular compras seleccionadas"
   - ✅ **Columna de estado** - Muestra badge de anulación
   - ✅ **Filtro** - Por estado anulada/activa
   - ✅ **Campos readonly** - `anulada` y `fecha_anulacion`

9. **Herramientas de Utilidad** ✅

   - ✅ **`revertir_anulacion.py`** - Management command para revertir anulaciones
   - ✅ **`crear_reversas_faltantes.py`** - Crea reversas para compras anuladas sin reversa
   - ✅ **`limpiar_datos_prueba.py`** - Elimina compras anuladas y movimientos de prueba
   - ✅ **`diagnostico_anulaciones.py`** - Diagnóstico de estado de anulaciones

**Archivos modificados:**

- [`Inventario/models.py`](file:///E:/AmandaBoutique/Inventario/models.py) - Campos y método `anular()`
- [`Inventario/signals.py`](file:///E:/AmandaBoutique/Inventario/signals.py) - Pre_save y post_save
- [`Inventario/views_grupo_compras.py`](file:///E:/AmandaBoutique/Inventario/views_grupo_compras.py) - Vista de anulación
- [`Inventario/urls.py`](file:///E:/AmandaBoutique/Inventario/urls.py) - Rutas actualizadas
- [`Inventario/admin.py`](file:///E:/AmandaBoutique/Inventario/admin.py) - Permisos y acción
- [`flujo/models.py`](file:///E:/AmandaBoutique/flujo/models.py) - Campo `numero_factura`

**Archivos creados:**

- [`Inventario/templates/Inventario/anular_compra.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/anular_compra.html)
- [`Inventario/templates/Inventario/anular_compra_grupo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/anular_compra_grupo.html)
- [`Inventario/management/commands/revertir_anulacion.py`](file:///E:/AmandaBoutique/Inventario/management/commands/revertir_anulacion.py)
- [`Inventario/management/commands/crear_reversas_faltantes.py`](file:///E:/AmandaBoutique/Inventario/management/commands/crear_reversas_faltantes.py)
- [`Inventario/management/commands/limpiar_datos_prueba.py`](file:///E:/AmandaBoutique/Inventario/management/commands/limpiar_datos_prueba.py)
- [`Inventario/management/commands/diagnostico_anulaciones.py`](file:///E:/AmandaBoutique/Inventario/management/commands/diagnostico_anulaciones.py)

**Flujo completo de anulación:**

```
1. Usuario hace clic en "Anular" en listado de compras
2. Se muestra template de confirmación con detalles
3. Usuario confirma anulación
4. Vista llama a compra.anular():
   a. Marca anulada = True
   b. Establece fecha_anulacion = now()
   c. Revierte inventario (resta cantidad)
   d. Guarda la compra
5. Pre_save signal captura estado anterior (anulada=False)
6. Post_save signal detecta cambio de False a True
7. Post_save crea MovimientoCaja de reversa:
   - Tipo: Ingreso
   - Descripción: "REVERSA - Anulación Factura [NÚMERO]"
   - Monto: Mismo que compra original
   - Fecha: Fecha de la compra
8. Usuario ve mensaje de éxito
9. Listado muestra badge "ANULADA"
10. Movimientos de caja muestra badge "REVERSA"
```

**Impacto:**

- ✅ **Trazabilidad completa** - Nunca se pierde información
- ✅ **Auditoría** - Historial completo de operaciones
- ✅ **Integridad financiera** - Movimientos compensados automáticamente
- ✅ **Inventario preciso** - Reversión automática de cantidades
- ✅ **Indicadores visuales** - Fácil identificación de anulaciones
- ✅ **Seguridad** - Solo superusuarios pueden eliminar permanentemente
- ✅ **Comandos de utilidad** - Herramientas para gestión y diagnóstico

### 📊 Reportes y PDFs (Dic 7-9)

#### **Mejoras en Generación de PDFs** ✅

- ✅ **Headers repetidos** - En todas las páginas de reportes largos
- ✅ **Formato estandarizado** - Diseño consistente en todos los PDFs
- ✅ **Espaciado optimizado** - Mejor uso del espacio en página
- ✅ **Alineación correcta** - Columnas numéricas alineadas a la derecha
- ✅ **Formato de números** - Miles con punto, decimales con coma
- ✅ **Filtros visibles** - Filtros aplicados mostrados en header del PDF

**PDFs mejorados:**

- Reporte de Movimientos Financieros
- Estado de Cuenta Bancaria
- Estado de Cuenta Efectivo
- Reporte de Pagos
- Catálogo de productos

#### **Nuevos Reportes Financieros** ✅

- ✅ **Estado de Cuenta Bancaria** - Con filtros y exportación PDF
- ✅ **Estado de Cuenta Efectivo** - Con filtros y exportación PDF
- ✅ **Reporte Anual de Pagos** - Usando campo `mes_pago`

### 🔐 Sistema de Permisos y Usuarios (Dic 2024)

#### **Gestión Mejorada de Usuarios** ✅

- ✅ **Registro con permisos de solo lectura** - Por defecto
- ✅ **Gestión de permisos por superusuarios** - Interfaz dedicada
- ✅ **Permisos granulares por módulo:**
  - Ver (view)
  - Agregar (add)
  - Cambiar (change)
  - Eliminar (delete)
- ✅ **Eliminación de usuarios** - Solo no-superusuarios
- ✅ **Protección de vistas** - Con decoradores
- ✅ **UI adaptativa** - Según permisos del usuario
- ✅ **Corrección de templates** - Labels de campos correctos

### 🎯 Mejoras en Módulo de Citas (Dic 2024)

- ✅ **Calendario visual mejorado** - Con datos de entrega
- ✅ **Estados de citas** - Pendiente, Confirmada, Completada, Cancelada
- ✅ **Campos corregidos** - Todos los campos visibles en formularios
- ✅ **Botones estandarizados** - Consistentes con el resto del proyecto

### 🔧 Correcciones y Optimizaciones

#### **Correcciones de Bugs** ✅

- ✅ **TemplateSyntaxError** - Corregido en `movimientos_pdf.html`
- ✅ **get_moneda_display** - Error de template corregido
- ✅ **Campos duplicados** - Eliminados en formularios
- ✅ **Títulos incorrectos** - Corregidos en todas las vistas
- ✅ **Formato de fechas** - Estandarizado a dd/mm/yyyy

#### **Optimizaciones de Base de Datos** ✅

- ✅ **Campo mes_pago** - Agregado a modelo Pago
- ✅ **Lógica automática** - `mes_pago = Fecha_Pago` si está vacío
- ✅ **Validación de cotizaciones** - Al crear pagos en VES
- ✅ **Señales Django** - Creación automática de Movimientos
- ✅ **Script de actualización** - Tipos de transacción 'Efectivo' → 'Depósito'

#### **Mejoras de Interfaz** ✅

- ✅ **Imagen de fondo** - `Tunapuy.jpg` con transparencia en index
- ✅ **Paleta de colores consistente** - Rosa (#b76e79) en todo el proyecto
- ✅ **Terminología actualizada** - "Deudor" → "Pagos pendientes"
- ✅ **Navegación mejorada** - Link a Admin en menú Finanzas

### 🚀 Despliegue y Producción (Dic 6-10)

#### **Configuración de Servicios NSSM** ✅

**AmandaBoutique (Puerto 8000):**

- ✅ Servicio: DjangoServidor
- ✅ Estado: SERVICE_RUNNING
- ✅ IP: 192.168.1.193:8000

**AsoTunapuy (Puerto 9000):**

- ✅ Servicio: AsoTunapuy
- ✅ Estado: SERVICE_RUNNING
- ✅ IP: 192.168.1.193:9000
- ✅ Sugerencia de números de control (001-999)

#### **Scripts de Despliegue** ✅

- ✅ **actualizar_produccion_simple.ps1** - Actualización automatizada
- ✅ **start_service.ps1** - Inicio de servicios
- ✅ **Documentación completa** - Manuales de implementación

#### **Resolución de Problemas** ✅

- ✅ **Servicio pausado** - Solucionado
- ✅ **Errores de inicio** - Corregidos
- ✅ **Configuración de settings.py** - Optimizada para producción

---

## 🗂️ Estructura del Módulo Flujo

### Modelos ([`flujo/models.py`](file:///E:/AmandaBoutique/flujo/models.py))

#### `CotizacionDolar`

```python
- fecha: DateField (unique=True)
- valor: DecimalField (Bs por USD)
- Ordenado por: -fecha (más reciente primero)
```

#### `MovimientoCaja`

```python
- fecha: DateField
- descripcion: CharField(200)
- tipo: CharField (Ingreso/Gasto)
- monto: DecimalField
- moneda: CharField (Bs/$)
- monto_usd: DecimalField (calculado automáticamente)
```

**Lógica de conversión automática:**

- Si moneda = 'Bs': busca cotización del día y convierte a USD
- Si moneda = '$': monto_usd = monto
- Validación: requiere cotización existente para movimientos en Bs

### Vistas Principales

| Vista                 | Función                     | Estado      |
| --------------------- | --------------------------- | ----------- |
| `listar_movimientos`  | Lista todos los movimientos | ✅          |
| `crear_movimiento`    | Crea nuevo movimiento       | ✅          |
| `listar_cotizaciones` | Lista cotizaciones          | ✅          |
| `crear_cotizacion`    | Crea nueva cotización       | ✅          |
| `editar_cotizacion`   | Edita cotización existente  | ✅ Nuevo    |
| `eliminar_cotizacion` | Elimina cotización          | ✅ Nuevo    |
| `dashboard_flujo`     | Dashboard financiero        | ✅ Mejorado |
| `movimientos_pdf`     | Exporta a PDF               | ✅          |
| `movimientos_excel`   | Exporta a Excel             | ✅          |

### Templates

| Template                   | Propósito                                 |
| -------------------------- | ----------------------------------------- |
| `listar_movimientos.html`  | Lista de movimientos de caja              |
| `crear_movimiento.html`    | Formulario de nuevo movimiento            |
| `listar_cotizaciones.html` | Lista de cotizaciones con editar/eliminar |
| `crear_cotizacion.html`    | Formulario de nueva cotización            |
| `editar_cotizacion.html`   | Formulario de edición de cotización       |
| `dashboard.html`           | Dashboard con métricas y gráficos         |
| `movimientos_pdf.html`     | Template para exportación PDF             |

---

## 🔍 Archivos Modificados (Git Status)

```
M AmandaProjecto/settings.py
M BoutiqueApp/models.py
M BoutiqueApp/templates/BoutiqueApp/detalle_catalogo.html
M BoutiqueApp/templates/BoutiqueApp/index.html
M BoutiqueApp/templates/BoutiqueApp/listar_catalogo.html
M BoutiqueApp/views.py
M ClientesApp/templates/ClientesApp/cliente_pdf.html
?? flujo/templates/flujo/movimientos_pdf.html (nuevo)
```

---

## 🛠️ Tecnologías Utilizadas

- **Framework:** Django
- **Base de datos:** SQLite (`db.sqlite3`)
- **Servidor de producción:** Waitress
- **Servicio Windows:** NSSM (Non-Sucking Service Manager)
- **Generación PDF:** Weasyprint + gtk3-runtime
- **Gráficos:** Chart.js
- **Frontend:** Bootstrap + CSS personalizado

---

## 📊 Funcionalidades del Sistema

### Apps Principales

1. **BoutiqueApp** - Catálogo de vestidos y showroom
2. **ClientesApp** - Gestión de clientes
3. **ProveedoresApp** - Gestión de proveedores
4. **citas** - Sistema de citas y calendario
5. **flujo** - Control de flujo de efectivo (Mejorado recientemente)
6. **LoginApp** - Perfiles de usuario

### Características del Módulo Flujo

- ✅ Registro de ingresos y gastos
- ✅ Manejo dual de monedas (Bs y USD)
- ✅ Conversión automática usando cotizaciones
- ✅ Dashboard con métricas financieras
- ✅ Filtros por mes y año
- ✅ Gráficos de comportamiento anual
- ✅ Exportación a PDF y Excel
- ✅ CRUD completo de cotizaciones
- ✅ Validación de cotizaciones requeridas

---

## ⚠️ Puntos de Atención

### 1. **Validación de Cotizaciones**

El sistema requiere que exista una cotización del dólar para la fecha del movimiento cuando se registra en Bolívares. Esto previene errores de conversión.

### 2. **Cálculo de Rentabilidad**

La rentabilidad se calcula como: `(Saldo / Total Ingresos) × 100`

- Verde si es positiva
- Roja si es negativa

### 3. **Conversión a Bolívares (Estimada)**

Los totales en Bolívares son estimados porque:

- Movimientos en USD se multiplican por la cotización del día
- Si no hay cotización para ese día, usa factor 1

---

## 🚀 Acceso al Sistema

**URL:** http://192.168.1.193:8000

### Rutas del Módulo Flujo

- `/flujo/movimientos/` - Lista de movimientos
- `/flujo/movimientos/crear/` - Crear movimiento
- `/flujo/cotizaciones/` - Lista de cotizaciones
- `/flujo/cotizaciones/crear/` - Crear cotización
- `/flujo/cotizaciones/editar/<id>/` - Editar cotización
- `/flujo/cotizaciones/eliminar/<id>/` - Eliminar cotización
- `/flujo/dashboard/` - Dashboard financiero
- `/flujo/movimientos/pdf/` - Exportar PDF
- `/flujo/movimientos/excel/` - Exportar Excel

---

## 📝 Recomendaciones

### Mantenimiento

1. **Backups regulares** - La base de datos SQLite está en `E:\AmandaBoutique\db.sqlite3`
2. **Monitoreo del servicio** - Verificar estado con `C:\nssm\nssm.exe status DjangoServidor`
3. **Logs** - Revisar logs del servicio en caso de errores

### Actualizaciones Futuras

El script [`actualizar_produccion_simple.ps1`](file:///E:/AmandaBoutique/actualizar_produccion_simple.ps1) está disponible para desplegar cambios desde desarrollo a producción.

**Proceso:**

1. Detener servicio: `C:\nssm\nssm.exe stop DjangoServidor`
2. Copiar archivos actualizados
3. Ejecutar migraciones: `py manage.py migrate`
4. Recolectar estáticos: `py manage.py collectstatic --noinput`
5. Iniciar servicio: `C:\nssm\nssm.exe start DjangoServidor`

---

## ✨ Resumen de Mejoras Recientes

> [!IMPORTANT] > **Cambios implementados (Nov 28 - Dic 16, 2025):**
>
> ### 🎨 Estandarización y Diseño
>
> 1. ✅ Botones estandarizados en todos los módulos (colores, tamaños, ubicación)
> 2. ✅ Eliminación de iconos para interfaz más limpia
> 3. ✅ Templates formateados consistentemente
> 4. ✅ Estilos inline migrados a CSS externo
> 5. ✅ Terminología unificada ("Volver" en lugar de "Cancelar")
>
> ### 💰 Módulo Flujo de Caja
>
> 6. ✅ CRUD completo para cotizaciones del dólar
> 7. ✅ Dashboard financiero con rentabilidad y contadores
> 8. ✅ Conversión automática Bs → USD
> 9. ✅ Filtros avanzados (fecha, tipo, método, moneda)
> 10. ✅ Exportación mejorada a PDF y Excel
> 11. ✅ Gráficos interactivos con Chart.js
>
> ### 📦 Inventario de Insumos
>
> 12. ✅ Sistema completo de gestión de inventario
> 13. ✅ Compras con conversión automática de moneda
> 14. ✅ Uso de insumos con formulario dinámico
> 15. ✅ Cálculo automático de costos de producción
> 16. ✅ Alertas de stock mínimo
> 17. ✅ **NUEVO (Dic 15):** Campos de categoría y proveedor
> 18. ✅ **NUEVO (Dic 15):** Filtros por categoría y proveedor
> 19. ✅ **NUEVO (Dic 15):** Select2 para búsqueda rápida de insumos
> 20. ✅ **NUEVO (Dic 15):** Corrección de bug en edición de compras
> 21. ✅ **NUEVO (Dic 15):** Cálculo correcto de valor total en PDF
> 22. ✅ **NUEVO (Dic 16):** Compras agrupadas por número de factura
> 23. ✅ **NUEVO (Dic 16):** Edición de múltiples ítems con formset
> 24. ✅ **NUEVO (Dic 16):** Anulación de ítems individuales
> 25. ✅ **NUEVO (Dic 16):** Movimientos de caja automáticos
> 26. ✅ **NUEVO (Dic 16):** Sincronización inventario-flujo de caja
> 27. ✅ **NUEVO (Dic 17):** Sistema de anulación de compras
> 28. ✅ **NUEVO (Dic 17):** Movimientos de reversa automáticos
> 29. ✅ **NUEVO (Dic 17):** Trazabilidad completa (no elimina, anula)
> 30. ✅ **NUEVO (Dic 17):** Indicadores visuales de anulación
> 31. ✅ **NUEVO (Dic 17):** Pre_save y post_save signals mejorados
> 32. ✅ **NUEVO (Dic 17):** Comandos de utilidad para gestión
> 33. ✅ **NUEVO (Dic 17):** Mejoras en formateo de código HTML
> 34. ✅ **NUEVO (Dic 17):** Indentación consistente en templates
> 35. ✅ **NUEVO (Dic 17):** Espaciado correcto en Django template tags
> 36. ✅ **NUEVO (Dic 17):** Limpieza de código y estándares aplicados
>
> ### 📊 Reportes y PDFs
>
> 37. ✅ Headers repetidos en todas las páginas
> 38. ✅ Formato estandarizado y profesional
> 39. ✅ Nuevos reportes financieros (Estado de Cuenta Bancaria/Efectivo)
> 40. ✅ Alineación y formato de números mejorados
>
> ### 🔐 Permisos y Usuarios
>
> 41. ✅ Sistema de permisos granulares por módulo
> 42. ✅ Interfaz de gestión de usuarios mejorada
> 43. ✅ Registro con permisos de solo lectura por defecto
> 44. ✅ UI adaptativa según permisos
>
> ### 🔧 Correcciones y Optimizaciones
>
> 45. ✅ Múltiples bugs corregidos (TemplateSyntaxError, campos duplicados, etc.)
> 46. ✅ Base de datos optimizada (campo mes_pago, señales Django)
> 47. ✅ Formato de fechas estandarizado (dd/mm/yyyy)
> 48. ✅ Validaciones mejoradas en formularios
> 49. ✅ **NUEVO (Dic 16):** Limpieza de código (3 templates obsoletos eliminados)
> 50. ✅ **NUEVO (Dic 17):** Estándares de formateo HTML aplicados
>
> ### 🚀 Producción
>
> 51. ✅ Dos servicios NSSM configurados (AmandaBoutique:8000, AsoTunapuy:9000)
> 52. ✅ Scripts de despliegue automatizados
> 53. ✅ Documentación completa de implementación

---

## 📈 Estadísticas del Proyecto

### Módulos Activos

| Módulo         | Estado | Características Principales                              |
| -------------- | ------ | -------------------------------------------------------- |
| BoutiqueApp    | ✅     | Catálogo, exportación PDF, búsqueda                      |
| ClientesApp    | ✅     | Gestión de clientes, historial                           |
| ProveedoresApp | ✅     | Gestión de proveedores                                   |
| citas          | ✅     | Calendario interactivo, estados de citas                 |
| flujo          | ✅     | Dashboard financiero, cotizaciones, filtros, exportación |
| Inventario     | ✅     | Insumos, compras, usos, costos de producción             |
| LoginApp       | ✅     | Autenticación, permisos granulares, gestión de usuarios  |

### Tecnologías

- **Framework:** Django 5.1.4
- **Base de datos:** SQLite
- **Servidor:** Waitress (WSGI)
- **Servicio:** NSSM (Windows Service)
- **PDF:** Weasyprint + gtk3-runtime
- **Excel:** OpenPyXL
- **Gráficos:** Chart.js
- **Frontend:** Bootstrap 5 + CSS personalizado
- **Calendario:** FullCalendar.js

### Métricas de Calidad

- ✅ **100% de módulos** con botones estandarizados
- ✅ **100% de templates** formateados consistentemente
- ✅ **100% de vistas** protegidas con autenticación
- ✅ **Permisos granulares** en 7 módulos principales
- ✅ **Exportación PDF/Excel** en módulos clave
- ✅ **Validación de datos** en todos los formularios

---

## 🎯 Estado Actual del Sistema

**Estado general:** ✅ **Sistema funcionando correctamente en producción**

### Servicios en Ejecución

1. **AmandaBoutique** (192.168.1.193:8000)

   - Servicio: DjangoServidor
   - Estado: SERVICE_RUNNING ✅
   - Aplicación: Gestión de boutique completa

2. **AsoTunapuy** (192.168.1.193:9000)
   - Servicio: AsoTunapuy
   - Estado: SERVICE_RUNNING ✅
   - Aplicación: Sistema de asociación

### Funcionalidades Completadas

- ✅ Gestión completa de catálogo
- ✅ Sistema de citas con calendario
- ✅ Gestión de clientes y proveedores
- ✅ Flujo de caja con dashboard interactivo
- ✅ Inventario de insumos con costos
- ✅ Sistema de permisos granulares
- ✅ Exportación a PDF y Excel
- ✅ Reportes financieros avanzados
- ✅ Interfaz estandarizada y profesional

### Próximas Mejoras Planificadas

- [ ] Reportes avanzados con más gráficos
- [ ] Notificaciones automáticas de citas
- [ ] Historial de cambios por usuario (auditoría)
- [ ] Backup automático de base de datos
- [ ] API REST para integración con otros sistemas
- [ ] Dashboard ejecutivo con KPIs

---

## 📞 Información de Contacto y Soporte

**Versión del Sistema:** 2.6  
**Última Actualización:** 17 de diciembre de 2025  
**Desarrollado con:** Django 5.1.4 + Bootstrap 5  
**Documentación:** README.md actualizado con todas las funcionalidades

### Acceso al Sistema

- **Producción AmandaBoutique:** http://192.168.1.193:8000
- **Producción AsoTunapuy:** http://192.168.1.193:9000
- **Panel Admin:** /admin/

### Comandos Útiles

```powershell
# Verificar estado del servicio
C:\nssm\nssm.exe status DjangoServidor

# Detener servicio
C:\nssm\nssm.exe stop DjangoServidor

# Iniciar servicio
C:\nssm\nssm.exe start DjangoServidor

# Reiniciar servicio
C:\nssm\nssm.exe restart DjangoServidor

# Crear reversas para compras anuladas sin reversa
python manage.py crear_reversas_faltantes

# Revertir anulación de una factura específica
python manage.py revertir_anulacion [NUMERO_FACTURA]

# Limpiar datos de prueba (compras anuladas y movimientos)
python manage.py limpiar_datos_prueba --confirmar

# Diagnóstico de anulaciones
python manage.py diagnostico_anulaciones
```

### Backup de Base de Datos

```powershell
# Copiar base de datos
Copy-Item "E:\AmandaBoutique\db.sqlite3" -Destination "E:\Backups\db_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').sqlite3"
```

---

**Documento actualizado:** 17 de diciembre de 2025  
**Próxima revisión:** Enero 2026
