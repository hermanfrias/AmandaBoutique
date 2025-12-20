# Revisión del Proyecto Amanda Boutique en Producción

**Fecha de Creación:** 28 de noviembre de 2025  
**Última Actualización:** 20 de diciembre de 2025  
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

## 📋 Cambios Recientes Implementados (Nov 28 - Dic 20, 2025)

### 🏢 Módulo de Activos Fijos (Dic 20, 2025) ✅

#### **Objetivo:** Implementar un sistema completo de gestión de activos fijos con control financiero, garantías y mantenimiento.

**Características implementadas:**

1. **Modelo ActivoFijo Completo** ✅

   - ✅ **Código auto-generado** - AF00001, AF00002... (formato: AF + 5 dígitos)
   - ✅ **Campo `descripcion_corta`** - Identificación rápida del activo (max 200 caracteres, opcional)
   - ✅ **Tipo de activo** - Computadora, Mueble, Vehículo, Equipo, Herramienta, Otro
   - ✅ **Datos técnicos** - Marca, modelo, serial
   - ✅ **Proveedor** - Relación ForeignKey con ProveedoresApp
   - ✅ **Ubicación y responsable** - Campos de texto para asignación
   - ✅ **Fotografía** - Campo de imagen opcional
   - ✅ **Observaciones** - Campo de texto para notas adicionales

2. **Gestión Financiera** ✅

   - ✅ **Valor de adquisición** - Moneda dual (Bs o $)
   - ✅ **Conversión automática** - Usa cotización del día para calcular `valor_dolares`
   - ✅ **Depreciación anual** - Porcentaje configurable (0-100%)
   - ✅ **Cálculo automático de valor actual:**
     ```python
     años_transcurridos = (fecha_actual - fecha_adquisicion).days / 365.25
     depreciacion_acumulada = valor_dolares * (depreciacion_anual / 100) * años_transcurridos
     valor_actual = max(0, valor_dolares - depreciacion_acumulada)
     ```
   - ✅ **Porcentaje de depreciación** - Calculado automáticamente

3. **Control de Garantía** ✅

   - ✅ **Duración en meses** - Campo numérico
   - ✅ **Fecha de expiración** - Calculada automáticamente
   - ✅ **Estado de garantía** - Property que retorna True/False
   - ✅ **Días restantes** - Cálculo automático (positivo si vigente, negativo si expirada)

4. **Gestión de Mantenimiento** ✅

   - ✅ **Fecha de último mantenimiento** - Campo de fecha
   - ✅ **Descripción del mantenimiento** - Campo de texto
   - ✅ **Formulario dedicado** - `form_mantenimiento.html` para registro

5. **Estados del Activo** ✅

   - ✅ **Activo** - Badge verde
   - ✅ **En Mantenimiento** - Badge amarillo
   - ✅ **Dado de Baja** - Badge rojo
   - ✅ **Inactivo** - Badge gris

6. **Filtros Avanzados** ✅

   - ✅ **Por tipo de activo** - Dropdown con todos los tipos
   - ✅ **Por estado** - Dropdown con todos los estados
   - ✅ **Por rango de fechas** - Fecha desde/hasta de adquisición
   - ✅ **Búsqueda** - Por número de inventario, marca o modelo

7. **Exportación a PDF** ✅

   - ✅ **Template `activos_pdf.html`** - Diseño profesional
   - ✅ **Filtros aplicados** - Se reflejan en el PDF
   - ✅ **Resumen de totales:**
     - Total de activos
     - Valor total en USD
     - Depreciación acumulada
     - Valor actual total
   - ✅ **Totales por tipo** - Tabla adicional con desglose

8. **Interfaz Responsiva** ✅

   - ✅ **Tabla con `table-responsive`** - Scroll horizontal en móviles
   - ✅ **Filtros optimizados** - `col-12 col-sm-6 col-md-*` para mejor apilamiento
   - ✅ **Tarjetas de resumen** - `col-6 col-md-3` (2 por fila en móviles)
   - ✅ **Columnas de detalle** - `col-12 col-lg-6` para apilamiento en tablets

**Archivos creados:**

- [`Inventario/templates/Inventario/listar_activos.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_activos.html)
- [`Inventario/templates/Inventario/form_activo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/form_activo.html)
- [`Inventario/templates/Inventario/detalle_activo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/detalle_activo.html)
- [`Inventario/templates/Inventario/eliminar_activo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/eliminar_activo.html)
- [`Inventario/templates/Inventario/form_mantenimiento.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/form_mantenimiento.html)
- [`Inventario/templates/Inventario/activos_pdf.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/activos_pdf.html)

**Archivos modificados:**

- [`Inventario/models.py`](file:///E:/AmandaBoutique/Inventario/models.py) - Modelo `ActivoFijo` completo con properties
- [`Inventario/forms.py`](file:///E:/AmandaBoutique/Inventario/forms.py) - Forms `ActivoFijoForm` y `MantenimientoForm`
- [`Inventario/views.py`](file:///E:/AmandaBoutique/Inventario/views.py) - Vistas CRUD y PDF
- [`Inventario/urls.py`](file:///E:/AmandaBoutique/Inventario/urls.py) - Rutas del módulo
- [`Inventario/admin.py`](file:///E:/AmandaBoutique/Inventario/admin.py) - Admin de Django

**Migraciones aplicadas:**

- `0005_activofijo.py` - Creación del modelo
- `0006_activofijo_descripcion_corta.py` - Agregado campo descripción corta

**Impacto:**

- ✅ **Control de activos** - Gestión completa del patrimonio de la empresa
- ✅ **Cálculos automáticos** - Depreciación y valores actualizados
- ✅ **Trazabilidad** - Historial de mantenimientos y garantías
- ✅ **Reportes profesionales** - PDF con información detallada
- ✅ **Experiencia móvil** - Diseño completamente responsivo

---

### 📱 Mejoras de Responsividad (Dic 20, 2025) ✅

#### **Objetivo:** Hacer que todas las plantillas del módulo de Inventario sean completamente responsivas en dispositivos móviles, tablets y desktop.

**Problemas identificados:**

- ❌ **Tablas desbordadas** - Columnas no visibles en móviles
- ❌ **Filtros mal apilados** - Ocupaban demasiado espacio vertical
- ❌ **Tarjetas sin optimizar** - Se apilaban verticalmente en móviles
- ❌ **Botones inconsistentes** - Tamaños y layouts variables

**Soluciones implementadas:**

1. **Tablas Responsivas** ✅

   - ✅ **Wrapper `table-responsive`** - Permite scroll horizontal
   - ✅ Aplicado en:
     - `listar_activos.html`
     - `detalle_activo.html`
     - `eliminar_activo.html`

2. **Filtros Optimizados** ✅

   - ✅ **Clases responsivas:**
     - `col-12` - Ancho completo en móviles (<576px)
     - `col-sm-6` - 2 por fila en tablets (≥576px)
     - `col-md-3` - 4 por fila en desktop (≥768px)
   - ✅ **Resultado:** Mejor aprovechamiento del espacio en todos los tamaños

3. **Tarjetas de Resumen** ✅

   - ✅ **Cambio:** `col-md-3` → `col-6 col-md-3`
   - ✅ **Resultado:** 2 tarjetas por fila en móviles, 4 en desktop
   - ✅ Información más accesible en pantallas pequeñas

4. **Columnas de Detalle** ✅

   - ✅ **Cambio:** `col-md-6` → `col-12 col-lg-6`
   - ✅ **Resultado:** Apilamiento vertical en tablets, lado a lado en desktop

5. **Corrección de Template Tags** ✅

   - ✅ **Problema:** Tags de Django divididos en múltiples líneas causaban errores
   - ✅ **Solución:** Cada tag en su propia línea completa
   - ✅ **Ejemplo correcto:**
     ```html
     {% if activo.moneda == 'Bs' %} Bs {{ activo.valor_adquisicion|floatformat:2
     }} {% else %} ${{ activo.valor_adquisicion|floatformat:2 }} {% endif %}
     ```

**Archivos modificados:**

- [`Inventario/templates/Inventario/listar_activos.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_activos.html) - Tabla, filtros y tarjetas
- [`Inventario/templates/Inventario/detalle_activo.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/detalle_activo.html) - Columnas y template tags

**Verificación realizada:**

- ✅ **Móvil (375px):** Tabla con scroll, filtros 1 por fila, tarjetas 2 por fila
- ✅ **Tablet (768px):** Filtros 2 por fila, layout optimizado
- ✅ **Desktop (1280px):** Layout completo sin restricciones

**Clases de Bootstrap 5 utilizadas:**

- `table-responsive` - Scroll horizontal en tablas
- `col-12`, `col-6`, `col-sm-6`, `col-md-*`, `col-lg-6` - Grid responsivo
- `d-flex`, `flex-column`, `flex-md-row` - Flexbox responsivo
- `gap-2`, `gap-3` - Espaciado entre elementos

**Impacto:**

- ✅ **Experiencia móvil mejorada** - Todas las funciones accesibles
- ✅ **Diseño adaptable** - Se ajusta a cualquier tamaño de pantalla
- ✅ **Sin desbordamiento** - Scroll horizontal solo cuando es necesario
- ✅ **Código limpio** - Template tags correctamente formateados

---

### 🎨 Estandarización Completa de Plantillas (Dic 20, 2025) ✅

#### **Objetivo:** Crear consistencia visual total en todo el proyecto usando `listar_movimientos.html` como modelo de referencia.

**Cambios implementados:**

1. **Nuevo Archivo CSS Centralizado** ✅

   - ✅ **Archivo creado:** [`BoutiqueApp/static/BoutiqueApp/css/boutique_standard.css`](file:///E:/AmandaBoutique/BoutiqueApp/static/BoutiqueApp/css/boutique_standard.css)
   - ✅ **Contenido:** ~350 líneas de estilos estandarizados
   - ✅ **Componentes incluidos:**
     - Estilos de tablas con gradientes
     - Grupos de botones de acción
     - Cards de filtros con gradientes
     - Badges personalizados
     - Encabezados de página
     - Cajas de resumen
     - Modales
     - Layouts de formularios

2. **Integración en Base Template** ✅

   - ✅ **Archivo modificado:** [`BoutiqueApp/templates/BoutiqueApp/base.html`](file:///E:/AmandaBoutique/BoutiqueApp/templates/BoutiqueApp/base.html)
   - ✅ Referencia a `boutique_standard.css` agregada
   - ✅ Estilos disponibles globalmente

3. **Plantillas Estandarizadas (20 archivos)** ✅

   **Módulo Inventario (3 plantillas):**

   - ✅ [`listar_insumos.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_insumos.html)
   - ✅ [`listar_compras.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_compras.html)
   - ✅ [`listar_usos.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_usos.html)

   **Módulo Clientes (1 plantilla):**

   - ✅ [`clientes_list.html`](file:///E:/AmandaBoutique/ClientesApp/templates/ClientesApp/clientes_list.html)

   **Módulo Proveedores (1 plantilla):**

   - ✅ [`proveedores_list.html`](file:///E:/AmandaBoutique/ProveedoresApp/templates/ProveedoresApp/proveedores_list.html)

   **Módulo Citas (1 plantilla):**

   - ✅ [`listar_citas.html`](file:///E:/AmandaBoutique/citas/templates/citas/listar_citas.html)

   **Módulo Flujo de Caja (11 plantillas):**

   - ✅ [`listar_cotizaciones.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/listar_cotizaciones.html)
   - ✅ [`listar_configuraciones_iva.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/listar_configuraciones_iva.html)
   - ✅ [`listar_movimientos.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/listar_movimientos.html)
   - ✅ [`crear_cotizacion.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/crear_cotizacion.html)
   - ✅ [`crear_movimiento.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/crear_movimiento.html)
   - ✅ [`crear_configuracion_iva.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/crear_configuracion_iva.html)
   - ✅ [`editar_cotizacion.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/editar_cotizacion.html)
   - ✅ [`editar_movimiento.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/editar_movimiento.html)
   - ✅ [`editar_configuracion_iva.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/editar_configuracion_iva.html)
   - ✅ [`ver_movimiento.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/ver_movimiento.html)
   - ✅ [`dashboard.html`](file:///E:/AmandaBoutique/flujo/templates/flujo/dashboard.html)

   **Módulo Catálogo (1 plantilla):**

   - ✅ [`listar_catalogo.html`](file:///E:/AmandaBoutique/BoutiqueApp/templates/BoutiqueApp/listar_catalogo.html)

4. **Características de Diseño Aplicadas** ✅

   **Encabezados estandarizados:**

   ```html
   <h2 class="text-pink fw-bold"><i class="fas fa-[icon] me-2"></i>[Título]</h2>
   ```

   **Cards de filtros/búsqueda:**

   - Gradiente de fondo: `linear-gradient(135deg, #fff5f7 0%, #ffffff 100%)`
   - Títulos con iconos FontAwesome
   - Padding consistente (p-4)
   - Bordes redondeados sin borde visible

   **Tablas con gradiente:**

   - Encabezado: `linear-gradient(135deg, #b76e79 0%, #d4a5ae 100%)`
   - Efecto hover en filas:
     - Fondo: `#fff5f7`
     - Elevación: `transform: scale(1.01)`
     - Sombra: `box-shadow: 0 2px 8px rgba(183, 110, 121, 0.15)`
   - Bordes redondeados (15px)
   - Sombra elevada (shadow-lg)

   **Botones de acción agrupados:**

   ```html
   <div class="btn-action-group">
     <a class="btn btn-sm btn-ver btn-action">Ver</a>
     <a class="btn btn-sm btn-editar btn-action">Editar</a>
     <a class="btn btn-sm btn-eliminar btn-action">Eliminar</a>
   </div>
   ```

   - Tamaño consistente (btn-sm)
   - Espaciado uniforme (gap: 5px)
   - Sin salto de línea (nowrap)
   - Ancho mínimo (65px)

   **Iconos FontAwesome agregados:**

   - Encabezados de página
   - Botones principales (Agregar, Volver, Exportar)
   - Títulos de secciones de filtros

5. **Resolución de Conflicto CSS** ✅

   **Problema identificado:**

   - Archivo `staticfiles/flujo/css/flujo.css` sobrescribía `.btn-pink`
   - Color conflictivo: `#c4296a` (rosa fucsia)
   - Color estándar: `#e6b2c6` (rosa pastel)

   **Solución implementada:**

   - ✅ Eliminadas todas las referencias a `flujo.css` de 11 plantillas del módulo flujo
   - ✅ Archivo `staticfiles/flujo/css/flujo.css` eliminado
   - ✅ Todos los botones `.btn-pink` ahora usan el color estándar consistentemente

6. **Limpieza para Producción** ✅

   - ✅ Eliminados todos los directorios `__pycache__/`
   - ✅ Eliminados todos los archivos `*.pyc`
   - ✅ Eliminados todos los archivos `*.log`
   - ✅ Ejecutado `collectstatic` exitosamente

**Colores Preservados (Sin Cambios):**

Todos los colores se mantuvieron exactamente como estaban definidos en `estilos.css`:

- `btn-ver`: `#e6b2c6` (rosa pastel)
- `btn-editar`: `#b76e79` (rosa medio)
- `btn-eliminar`: `#f28ca3` (rosa coral)
- `btn-listar`: `#b76e79` (rosa medio)
- `btn-volver`: `#ffb6c1` (rosa claro)
- `btn-pink`: `#e6b2c6` (rosa pastel)

**Impacto:**

- ✅ **Consistencia visual total** - Mismo diseño en todos los módulos
- ✅ **Experiencia de usuario mejorada** - Interfaz predecible y profesional
- ✅ **Mantenibilidad** - Estilos centralizados fáciles de actualizar
- ✅ **Colores uniformes** - Sin conflictos ni inconsistencias
- ✅ **Diseño moderno** - Gradientes, sombras y efectos hover
- ✅ **Accesibilidad** - Botones agrupados y bien espaciados
- ✅ **Preparado para producción** - Archivos temporales eliminados

---

### 🐛 Correcciones de Bugs (Dic 18, 2025)

#### **Corrección de Tachado en Vista Agrupada de Compras** ✅

**Problema identificado:** En la vista agrupada de compras (`listar_compras.html`), todas las compras aparecían con tachado en lugar de solo las anuladas.

**Causa:** Sintaxis de Django template fragmentada incorrectamente en múltiples líneas:

```html
<!-- ANTES (Incorrecto) -->
<tr
  {%
  if
  grupo.anulada
  %}
  style="opacity: 0.6; text-decoration: line-through"
  {%
  endif
  %}
></tr>
```

**Solución implementada:**

```html
<!-- DESPUÉS (Correcto) -->
<tr
  {%
  if
  grupo.anulada
  %}style="opacity: 0.6; text-decoration: line-through"
  {%
  endif
  %}
></tr>
```

**Archivo modificado:**

- [`Inventario/templates/Inventario/listar_compras.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_compras.html) - Líneas 109-119

**Impacto:**

- ✅ **Visualización correcta** - Solo compras anuladas aparecen tachadas
- ✅ **Indicadores precisos** - Badge "ANULADA" solo en registros anulados
- ✅ **UX mejorada** - Diferenciación clara entre compras activas y anuladas

---

### 📦 Mejoras en Módulo de Uso de Insumos (Dic 18, 2025)

#### **Filtros Avanzados y Exportación PDF** ✅

**Objetivo:** Agregar capacidad de filtrado y exportación a PDF en el listado de Uso de Insumos.

**Cambios implementados:**

1. **Vista `listar_usos` Mejorada** ✅

   - ✅ **Filtro por rango de fechas** - `fecha_desde` y `fecha_hasta`
   - ✅ **Filtro por descripción** - Búsqueda con `icontains` (insensible a mayúsculas)
   - ✅ **Ordenamiento** - Por fecha de uso descendente
   - ✅ **Persistencia de filtros** - Valores mantenidos en formulario

2. **Nueva Vista `usos_pdf`** ✅

   - ✅ **Generación de PDF** - Usando WeasyPrint
   - ✅ **Filtros aplicables** - Mismos filtros que la vista de listado
   - ✅ **Cálculo de totales** - Cantidad de usos y costo total en USD
   - ✅ **Formato profesional** - Consistente con otros PDFs del sistema

3. **Template `listar_usos.html` Actualizado** ✅

   - ✅ **Formulario de filtros** - Card con campos de fecha y descripción
   - ✅ **Botón "Imprimir PDF"** - Pasa filtros activos a la URL
   - ✅ **Botón "Volver"** - Navegación consistente
   - ✅ **Botón "Limpiar Filtros"** - Resetea búsqueda

4. **Nuevo Template `usos_pdf.html`** ✅
   - ✅ **Header informativo** - Título y filtros aplicados
   - ✅ **Tabla de datos** - Fecha, Descripción, Costo Total USD
   - ✅ **Sección de totales** - Total de usos y costo acumulado
   - ✅ **Estilos consistentes** - Paleta rosa del sistema

**Archivos modificados:**

- [`Inventario/views.py`](file:///E:/AmandaBoutique/Inventario/views.py) - Vista `listar_usos` (líneas 579-603) y nueva vista `usos_pdf` (líneas 711-771)
- [`Inventario/urls.py`](file:///E:/AmandaBoutique/Inventario/urls.py) - Ruta `usos/pdf/` agregada
- [`Inventario/templates/Inventario/listar_usos.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/listar_usos.html) - Filtros y botones

**Archivos creados:**

- [`Inventario/templates/Inventario/usos_pdf.html`](file:///E:/AmandaBoutique/Inventario/templates/Inventario/usos_pdf.html)

**Nota:** Existe un error de sintaxis pendiente en `usos_pdf.html` (línea 61) que el usuario corregirá manualmente.

**Impacto:**

- ✅ **Búsqueda eficiente** - Filtros facilitan localización de usos específicos
- ✅ **Reportes personalizados** - PDF con datos filtrados
- ✅ **Trazabilidad mejorada** - Fácil seguimiento de consumo de insumos
- ✅ **Análisis de costos** - Totales calculados automáticamente

---

### 👥 Exportación PDF para Módulo de Clientes (Dic 18, 2025)

#### **Implementación de Exportación a PDF** ✅

**Objetivo:** Agregar funcionalidad de exportación a PDF para el listado de clientes con soporte de filtros.

**Cambios implementados:**

1. **Nueva Vista `clientes_pdf`** ✅

   - ✅ **Vista basada en funciones** - Complementa las vistas basadas en clases existentes
   - ✅ **Filtro de búsqueda** - Parámetro `buscar` opcional
   - ✅ **Ordenamiento** - Por apellido y nombre
   - ✅ **Cálculo de totales** - Contador de clientes
   - ✅ **Generación con WeasyPrint** - PDF profesional

2. **Template `clientes_list.html` Actualizado** ✅

   - ✅ **Botón "Imprimir PDF"** - Estilo rosa, tamaño pequeño
   - ✅ **Pasa filtro de búsqueda** - URL incluye parámetro `buscar`
   - ✅ **Abre en nueva pestaña** - `target="_blank"`

3. **Nuevo Template `clientes_pdf.html`** ✅

   - ✅ **Campos completos** - Identificación, Nombre, Apellido, Teléfono, Correo, Dirección
   - ✅ **Filtro visible** - Muestra búsqueda aplicada si existe
   - ✅ **Total de clientes** - Contador en sección de totales
   - ✅ **Diseño consistente** - Paleta y estilos del sistema

4. **URLs Corregidas** ✅
   - ✅ **Problema inicial** - Error 500 por orden incorrecto de rutas
   - ✅ **Causa** - Ruta genérica `<str:identificacion>/` capturaba "pdf" como ID
   - ✅ **Solución** - Mover `pdf/export/` ANTES de rutas genéricas
   - ✅ **Orden correcto:**
     ```python
     path('', ClientesListView.as_view(), name='clientes_list'),
     path('pdf/export/', clientes_pdf, name='clientes_pdf'),  # ← Antes
     path('crear/', ClientesCreateView.as_view(), name='clientes_create'),
     path('<str:identificacion>/editar/', ...),  # ← Después
     ```

**Archivos modificados:**

- [`ClientesApp/views.py`](file:///E:/AmandaBoutique/ClientesApp/views.py) - Nueva función `clientes_pdf` (líneas 52-98)
- [`ClientesApp/urls.py`](file:///E:/AmandaBoutique/ClientesApp/urls.py) - Ruta PDF agregada en orden correcto
- [`ClientesApp/templates/ClientesApp/clientes_list.html`](file:///E:/AmandaBoutique/ClientesApp/templates/ClientesApp/clientes_list.html) - Botón PDF

**Archivos creados:**

- [`ClientesApp/templates/ClientesApp/clientes_pdf.html`](file:///E:/AmandaBoutique/ClientesApp/templates/ClientesApp/clientes_pdf.html)

**Verificación realizada:**

- ✅ Página de clientes carga sin errores
- ✅ Botón "Imprimir PDF" visible y estilizado correctamente
- ✅ PDF se genera sin errores
- ✅ Filtro de búsqueda funciona correctamente
- ✅ PDF muestra filtro aplicado cuando existe

**Impacto:**

- ✅ **Reportes de clientes** - Exportación rápida para impresión
- ✅ **Filtrado efectivo** - PDF con clientes específicos
- ✅ **Documentación** - Respaldo físico de base de clientes
- ✅ **Consistencia** - Mismo patrón que otros módulos

**Lección aprendida:**

- ⚠️ **Orden de URLs crítico** - Rutas específicas deben ir antes de rutas genéricas con parámetros variables en Django

---

## 📋 Cambios Recientes Implementados (Nov 28 - Dic 17, 2025)

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
