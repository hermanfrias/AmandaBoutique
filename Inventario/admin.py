from django.contrib import admin
from .models import ExistenciaInsumo, CompraInsumo, UsoInsumo, DetalleUsoInsumo, ActivoFijo


@admin.register(ExistenciaInsumo)
class ExistenciaInsumoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'medida', 'existencia', 'existencia_minima', 'costo_dolar', 'fecha_creacion']
    list_filter = ['medida', 'fecha_creacion']
    search_fields = ['codigo', 'descripcion']
    readonly_fields = ['codigo', 'fecha_creacion']
    ordering = ['codigo']


@admin.register(CompraInsumo)
class CompraInsumoAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'fecha_compra', 'insumo', 'cantidad', 'moneda', 'monto', 'aplicar_iva', 'monto_total_usd', 'estado_anulacion']
    list_filter = ['numero_factura', 'moneda', 'aplicar_iva', 'anulada', 'fecha_compra']
    search_fields = ['numero_factura', 'insumo__codigo', 'insumo__descripcion']
    readonly_fields = ['monto_bs', 'monto_usd', 'monto_iva_bs', 'monto_iva_usd', 'monto_total_bs', 'monto_total_usd', 'anulada', 'fecha_anulacion']
    ordering = ['-fecha_compra']
    date_hierarchy = 'fecha_compra'
    actions = ['anular_compras_seleccionadas']
    
    fieldsets = (
        ('Información General', {
            'fields': ('numero_factura', 'insumo', 'fecha_compra', 'cantidad')
        }),
        ('Información de Pago', {
            'fields': ('moneda', 'monto', 'aplicar_iva')
        }),
        ('Montos Calculados (Solo Lectura)', {
            'fields': ('monto_bs', 'monto_usd', 'monto_iva_bs', 'monto_iva_usd', 'monto_total_bs', 'monto_total_usd'),
            'classes': ('collapse',),
        }),
        ('Estado de Anulación', {
            'fields': ('anulada', 'fecha_anulacion'),
            'classes': ('collapse',),
        }),
    )
    
    def estado_anulacion(self, obj):
        """Muestra el estado de anulación con badge"""
        if obj.anulada:
            return f'🚫 ANULADA ({obj.fecha_anulacion.strftime("%d/%m/%Y %H:%M")})'
        return '✅ Activa'
    estado_anulacion.short_description = 'Estado'
    
    def has_delete_permission(self, request, obj=None):
        """Permite eliminación solo a superusuarios (para pruebas en desarrollo)"""
        return request.user.is_superuser
    
    def anular_compras_seleccionadas(self, request, queryset):
        """Acción personalizada para anular compras desde el admin"""
        anuladas = 0
        ya_anuladas = 0
        errores = 0
        
        for compra in queryset:
            if compra.anulada:
                ya_anuladas += 1
            else:
                try:
                    compra.anular()
                    anuladas += 1
                except Exception as e:
                    errores += 1
                    self.message_user(request, f'Error al anular compra {compra.pk}: {str(e)}', level='ERROR')
        
        if anuladas > 0:
            self.message_user(request, f'{anuladas} compra(s) anulada(s) exitosamente. Se crearon movimientos de reversa.', level='SUCCESS')
        if ya_anuladas > 0:
            self.message_user(request, f'{ya_anuladas} compra(s) ya estaban anuladas.', level='WARNING')
        if errores > 0:
            self.message_user(request, f'{errores} error(es) al anular compras.', level='ERROR')
    
    anular_compras_seleccionadas.short_description = "Anular compras seleccionadas"



class DetalleUsoInsumoInline(admin.TabularInline):
    model = DetalleUsoInsumo
    extra = 1
    fields = ['insumo', 'cantidad', 'costo_unitario_usd', 'costo_total_usd']
    readonly_fields = ['costo_unitario_usd', 'costo_total_usd']


@admin.register(UsoInsumo)
class UsoInsumoAdmin(admin.ModelAdmin):
    list_display = ['fecha_uso', 'descripcion', 'costo_total_usd']
    list_filter = ['fecha_uso']
    search_fields = ['descripcion']
    date_hierarchy = 'fecha_uso'
    readonly_fields = ['costo_total_usd']
    inlines = [DetalleUsoInsumoInline]


# ============================================
# ADMIN: ACTIVO FIJO
# ============================================

@admin.register(ActivoFijo)
class ActivoFijoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_inventario', 'tipo_activo', 'marca', 'modelo',
        'valor_adquisicion', 'valor_dolares', 'valor_actual', 
        'estado', 'fecha_adquisicion'
    ]
    list_filter = ['tipo_activo', 'estado', 'moneda', 'fecha_adquisicion']
    search_fields = ['numero_inventario', 'marca', 'modelo', 'serial', 'ubicacion', 'responsable']
    readonly_fields = [
        'numero_inventario', 'valor_dolares', 'depreciacion_acumulada', 
        'valor_actual', 'fecha_creacion', 'fecha_actualizacion'
    ]
    date_hierarchy = 'fecha_adquisicion'
    ordering = ['-fecha_adquisicion', 'numero_inventario']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('numero_inventario', 'tipo_activo', 'marca', 'modelo', 'serial')
        }),
        ('Adquisición', {
            'fields': ('fecha_adquisicion', 'moneda', 'valor_adquisicion', 'valor_dolares')
        }),
        ('Depreciación', {
            'fields': ('depreciacion_anual', 'depreciacion_acumulada', 'valor_actual')
        }),
        ('Estado y Ubicación', {
            'fields': ('estado', 'ubicacion', 'responsable', 'foto')
        }),
        ('Mantenimiento', {
            'fields': ('fecha_mantenimiento', 'descripcion_mantenimiento'),
            'classes': ('collapse',),
        }),
        ('Información Adicional', {
            'fields': ('observaciones', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )
    
    def get_queryset(self, request):
        """Optimizar consultas"""
        qs = super().get_queryset(request)
        return qs.select_related()
