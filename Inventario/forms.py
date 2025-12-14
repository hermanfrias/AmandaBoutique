from django import forms
from .models import ExistenciaInsumo, CompraInsumo, UsoInsumo, DetalleUsoInsumo
from flujo.models import CotizacionDolar


class ExistenciaInsumoForm(forms.ModelForm):
    class Meta:
        model = ExistenciaInsumo
        fields = ['descripcion', 'medida', 'existencia', 'existencia_minima', 'costo_dolar']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'medida': forms.Select(attrs={'class': 'form-select'}),
            'existencia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'existencia_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'costo_dolar': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'descripcion': 'Descripción',
            'medida': 'Unidad de Medida',
            'existencia': 'Existencia',
            'existencia_minima': 'Existencia Mínima',
            'costo_dolar': 'Costo Unitario (USD)',
        }


class CompraInsumoForm(forms.ModelForm):
    class Meta:
        model = CompraInsumo
        fields = ['insumo', 'fecha_compra', 'cantidad', 'moneda', 'monto', 'aplicar_iva']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_compra': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'aplicar_iva': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'insumo': 'Insumo',
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
