from django.contrib import admin
from .models import Vestido, Alquiler


@admin.register(Vestido)
class VestidoAdmin(admin.ModelAdmin):
    list_display = ['nombre_modelo', 'talla', 'color', 'precio_alquiler', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'talla']
    search_fields = ['nombre_modelo', 'descripcion', 'color']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre_modelo', 'descripcion', 'talla', 'color', 'estado')
        }),
        ('Precios', {
            'fields': ('precio_alquiler', 'valor_compra')
        }),
        ('Fotos', {
            'fields': ('foto1', 'foto2')
        }),
        ('Información Adicional', {
            'fields': ('accesorios',)
        }),
        ('Tintorería', {
            'fields': ('fecha_tintoreria', 'fecha_entrega_tintoreria')
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'vestido', 'fecha_inicio', 'fecha_devolucion_prevista', 'tipo_moneda', 'monto_final', 'deposito', 'total_usd', 'estado_pago', 'estado_alquiler']
    list_filter = ['estado_pago', 'estado_alquiler', 'tipo_moneda', 'fecha_contrato']
    search_fields = ['cliente__nombre', 'cliente__apellido', 'vestido__nombre_modelo', 'notas']
    date_hierarchy = 'fecha_contrato'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Alquiler', {
            'fields': ('cliente', 'vestido')
        }),
        ('Fechas', {
            'fields': ('fecha_contrato', 'fecha_inicio', 'fecha_devolucion_prevista', 'fecha_devolucion_real')
        }),
        ('Montos', {
            'fields': ('tipo_moneda', 'anticipo', 'monto_final', 'deposito', 'total_usd')
        }),
        ('Estados', {
            'fields': ('estado_pago', 'estado_alquiler')
        }),
        ('Notas', {
            'fields': ('notas',)
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
