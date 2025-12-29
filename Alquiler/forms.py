from django import forms
from .models import Vestido, Alquiler
from ClientesApp.models import Clientes
from django.core.exceptions import ValidationError


class VestidoForm(forms.ModelForm):
    """Formulario para crear y editar vestidos"""
    
    class Meta:
        model = Vestido
        fields = [
            'nombre_modelo', 'descripcion', 'talla', 'color',
            'precio_alquiler', 'valor_compra', 'deposito_garantia',
            'estado', 'foto1', 'foto2', 'foto3', 'foto4', 'accesorios',
            'fecha_tintoreria', 'fecha_entrega_tintoreria'
        ]
        widgets = {
            'nombre_modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'talla': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_alquiler': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deposito_garantia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'foto1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'foto2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'foto3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'foto4': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'accesorios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fecha_tintoreria': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'fecha_entrega_tintoreria': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que las fechas se muestren correctamente al editar
        if self.instance and self.instance.pk:
            if self.instance.fecha_tintoreria:
                self.initial['fecha_tintoreria'] = self.instance.fecha_tintoreria.strftime('%Y-%m-%d')
            if self.instance.fecha_entrega_tintoreria:
                self.initial['fecha_entrega_tintoreria'] = self.instance.fecha_entrega_tintoreria.strftime('%Y-%m-%d')


class AlquilerForm(forms.ModelForm):
    """Formulario para crear y editar alquileres"""
    
    class Meta:
        model = Alquiler
        fields = [
            'cliente', 'vestido', 'fecha_contrato', 'fecha_inicio',
            'fecha_devolucion_prevista', 'fecha_devolucion_real',
            'tipo_moneda', 'anticipo', 'monto_final', 'deposito', 'pago_final',
            'estado_pago', 'estado_alquiler', 'notas'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'vestido': forms.Select(attrs={'class': 'form-select'}),
            'fecha_contrato': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'fecha_devolucion_prevista': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'fecha_devolucion_real': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'tipo_moneda': forms.Select(attrs={'class': 'form-select'}),
            'anticipo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monto_final': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deposito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pago_final': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado_pago': forms.Select(attrs={'class': 'form-select'}),
            'estado_alquiler': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo vestidos disponibles para nuevos alquileres
        if not self.instance.pk:
            self.fields['vestido'].queryset = Vestido.objects.filter(estado='Disponible')
        
        # Ordenar clientes por apellido
        self.fields['cliente'].queryset = Clientes.objects.all().order_by('apellido', 'nombre')
        
        # Asegurar que las fechas se muestren correctamente al editar
        if self.instance and self.instance.pk:
            if self.instance.fecha_contrato:
                self.initial['fecha_contrato'] = self.instance.fecha_contrato.strftime('%Y-%m-%d')
            if self.instance.fecha_inicio:
                self.initial['fecha_inicio'] = self.instance.fecha_inicio.strftime('%Y-%m-%d')
            if self.instance.fecha_devolucion_prevista:
                self.initial['fecha_devolucion_prevista'] = self.instance.fecha_devolucion_prevista.strftime('%Y-%m-%d')
            if self.instance.fecha_devolucion_real:
                self.initial['fecha_devolucion_real'] = self.instance.fecha_devolucion_real.strftime('%Y-%m-%d')


class ClienteRapidoForm(forms.ModelForm):
    """Formulario simplificado para crear clientes desde el formulario de alquiler"""
    
    class Meta:
        model = Clientes
        fields = ['identificacion', 'nombre', 'apellido', 'email', 'telefono', 'direccion']
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
