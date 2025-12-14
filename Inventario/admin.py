from django.contrib import admin
from .models import ExistenciaInsumo, CompraInsumo, UsoInsumo, DetalleUsoInsumo


@admin.register(ExistenciaInsumo)
class ExistenciaInsumoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'medida', 'existencia', 'existencia_minima', 'costo_dolar', 'fecha_creacion']
    list_filter = ['medida', 'fecha_creacion']
    search_fields = ['codigo', 'descripcion']
    readonly_fields = ['codigo', 'fecha_creacion']
    ordering = ['codigo']


@admin.register(CompraInsumo)
class CompraInsumoAdmin(admin.ModelAdmin):
    list_display = ['fecha_compra', 'insumo', 'cantidad', 'moneda', 'monto', 'aplicar_iva', 'monto_total_usd']
    list_filter = ['moneda', 'aplicar_iva', 'fecha_compra']
    search_fields = ['insumo__codigo', 'insumo__descripcion']
    readonly_fields = ['monto_bs', 'monto_usd', 'monto_iva_bs', 'monto_iva_usd', 'monto_total_bs', 'monto_total_usd']
    ordering = ['-fecha_compra']
    date_hierarchy = 'fecha_compra'
    
    fieldsets = (
        ('Información General', {
            'fields': ('insumo', 'fecha_compra', 'cantidad')
        }),
        ('Información de Pago', {
            'fields': ('moneda', 'monto', 'aplicar_iva')
        }),
        ('Montos Calculados (Solo Lectura)', {
            'fields': ('monto_bs', 'monto_usd', 'monto_iva_bs', 'monto_iva_usd', 'monto_total_bs', 'monto_total_usd'),
            'classes': ('collapse',),
        }),
    )


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
