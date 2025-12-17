from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MovimientoCaja)
admin.site.register(CotizacionDolar)


@admin.register(ConfiguracionIVA)
class ConfiguracionIVAAdmin(admin.ModelAdmin):
    list_display = ['fecha_inicio', 'porcentaje', 'activo']
    list_filter = ['activo']
    ordering = ['-fecha_inicio']
    list_editable = ['activo']
