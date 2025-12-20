from django import forms
from .models import ExistenciaInsumo, CompraInsumo, UsoInsumo, DetalleUsoInsumo, ActivoFijo
from flujo.models import CotizacionDolar


class ExistenciaInsumoForm(forms.ModelForm):
    class Meta:
        model = ExistenciaInsumo
        fields = ['descripcion', 'medida', 'existencia', 'existencia_minima', 'costo_dolar', 'proveedor', 'categoria']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '150'}),
            'medida': forms.Select(attrs={'class': 'form-select'}),
            'existencia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'existencia_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'costo_dolar': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'descripcion': 'Descripción',
            'medida': 'Unidad de Medida',
            'existencia': 'Existencia',
            'existencia_minima': 'Existencia Mínima',
            'costo_dolar': 'Costo Unitario (USD)',
            'proveedor': 'Proveedor',
            'categoria': 'Categoría',
        }


class CompraInsumoForm(forms.ModelForm):
    class Meta:
        model = CompraInsumo
        fields = ['insumo', 'numero_factura', 'fecha_compra', 'cantidad', 'moneda', 'monto', 'aplicar_iva']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-select'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: F-001234'}),
            'fecha_compra': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'aplicar_iva': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'insumo': 'Insumo',
            'numero_factura': 'Número de Factura',
            'fecha_compra': 'Fecha de Compra',
            'cantidad': 'Cantidad',
            'moneda': 'Moneda',
            'monto': 'Monto',
            'aplicar_iva': 'Aplicar IVA (16%)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el queryset del campo insumo para mostrar código y descripción
        self.fields['insumo'].queryset = ExistenciaInsumo.objects.all()
        self.fields['insumo'].label_from_instance = lambda obj: f"{obj.codigo} - {obj.descripcion}"

    def clean(self):
        cleaned_data = super().clean()
        fecha_compra = cleaned_data.get('fecha_compra')
        
        if fecha_compra:
            # Verificar que existe cotización para la fecha
            if not CotizacionDolar.objects.filter(fecha=fecha_compra).exists():
                raise forms.ValidationError(
                    f'No existe cotización del dólar para la fecha {fecha_compra.strftime("%d/%m/%Y")}. '
                    'Por favor registre la cotización del día primero en el módulo de Flujo de Caja.'
                )
        
        return cleaned_data


# Formulario para líneas de detalle en creación por lotes
class CompraInsumoDetalleForm(forms.Form):
    insumo = forms.ModelChoiceField(
        queryset=ExistenciaInsumo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select insumo-select'}),
        label='Insumo',
        required=False
    )
    cantidad = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'step': '0.01', 'min': '0.01'}),
        label='Cantidad',
        required=False
    )
    monto = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control monto-input', 'step': '0.01', 'min': '0.01'}),
        label='Monto',
        required=False
    )
    aplicar_iva = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input aplicar-iva-item'}),
        label='IVA'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['insumo'].label_from_instance = lambda obj: f"{obj.codigo} - {obj.descripcion}"


# Formset para crear múltiples compras
CompraInsumoDetalleFormSet = forms.formset_factory(
    CompraInsumoDetalleForm,
    extra=3,
    can_delete=True,
    min_num=1,
)


class UsoInsumoForm(forms.ModelForm):
    class Meta:
        model = UsoInsumo
        fields = ['fecha_uso', 'descripcion']
        widgets = {
            'fecha_uso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Vestido para cliente María'}),
        }
        labels = {
            'fecha_uso': 'Fecha de Uso',
            'descripcion': 'Descripción',
        }


class DetalleUsoInsumoForm(forms.ModelForm):
    class Meta:
        model = DetalleUsoInsumo
        fields = ['insumo', 'cantidad']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-select insumo-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'step': '0.01', 'min': '0.01'}),
        }
        labels = {
            'insumo': 'Insumo',
            'cantidad': 'Cantidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el queryset del campo insumo para mostrar código, descripción y existencia
        self.fields['insumo'].queryset = ExistenciaInsumo.objects.all()
        self.fields['insumo'].label_from_instance = lambda obj: f"{obj.codigo} - {obj.descripcion} (Disponible: {obj.existencia} {obj.medida})"


# Formset para agregar múltiples detalles de uso
DetalleUsoInsumoFormSet = forms.inlineformset_factory(
    UsoInsumo,
    DetalleUsoInsumo,
    form=DetalleUsoInsumoForm,
    extra=3,  # 3 formularios vacíos por defecto
    can_delete=True,
    min_num=1,  # Al menos un insumo es requerido
    validate_min=True,
)


# ============================================
# FORMULARIOS: ACTIVO FIJO
# ============================================

class ActivoFijoForm(forms.ModelForm):
    class Meta:
        model = ActivoFijo
        fields = [
            'descripcion_corta', 'fecha_adquisicion', 'tipo_activo', 'marca', 'modelo',
            'serial', 'proveedor', 'moneda', 'valor_adquisicion', 'depreciacion_anual',
            'garantia_meses', 'estado', 'ubicacion', 'responsable', 'foto', 'observaciones'
        ]
        widgets = {
            'descripcion_corta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Computadora portátil para diseño'}),
            'fecha_adquisicion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_activo': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: HP, Dell, Toyota'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pavilion 15, Camry'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie único'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'valor_adquisicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'depreciacion_anual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100', 'placeholder': 'Ej: 20.00 para 20%'}),
            'garantia_meses': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Ej: 12, 24, 36'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Oficina Principal, Almacén'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del responsable'}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales...'}),
        }
        labels = {
            'descripcion_corta': 'Descripción Corta',
            'fecha_adquisicion': 'Fecha de Adquisición',
            'tipo_activo': 'Tipo de Activo',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'serial': 'Serial',
            'proveedor': 'Proveedor',
            'moneda': 'Moneda',
            'valor_adquisicion': 'Valor de Adquisición',
            'depreciacion_anual': 'Depreciación Anual (%)',
            'garantia_meses': 'Garantía (meses)',
            'estado': 'Estado',
            'ubicacion': 'Ubicación',
            'responsable': 'Responsable',
            'foto': 'Foto del Activo',
            'observaciones': 'Observaciones',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_adquisicion = cleaned_data.get('fecha_adquisicion')
        moneda = cleaned_data.get('moneda')
        
        # Validar que existe cotización si la moneda es Bs
        if fecha_adquisicion and moneda == 'Bs':
            if not CotizacionDolar.objects.filter(fecha=fecha_adquisicion).exists():
                raise forms.ValidationError(
                    f'No existe cotización del dólar para la fecha {fecha_adquisicion.strftime("%d/%m/%Y")}. '
                    'Por favor registre la cotización del día primero en el módulo de Flujo de Caja.'
                )
        
        return cleaned_data


class MantenimientoForm(forms.ModelForm):
    """Formulario rápido para registrar mantenimiento de un activo"""
    class Meta:
        model = ActivoFijo
        fields = ['fecha_mantenimiento', 'descripcion_mantenimiento']
        widgets = {
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion_mantenimiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describa el mantenimiento realizado...'}),
        }
        labels = {
            'fecha_mantenimiento': 'Fecha de Mantenimiento',
            'descripcion_mantenimiento': 'Descripción del Mantenimiento',
        }
