from django import forms
from .models import MovimientoCaja, CotizacionDolar, ConfiguracionIVA

class MovimientoCajaForm(forms.ModelForm):
    class Meta:
        model = MovimientoCaja
        fields = ['fecha', 'descripcion', 'tipo', 'moneda', 'monto', 'tipo_movimiento', 'metodo_pago']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date','class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-select'}),
            'moneda': forms.Select(attrs={'class':'form-select'}),
            'monto': forms.NumberInput(attrs={'class':'form-control'}),
            'tipo_movimiento': forms.Select(attrs={'class':'form-select'}),
            'metodo_pago': forms.Select(attrs={'class':'form-select'}),
        }



class CotizacionDolarForm(forms.ModelForm):
    class Meta:
        model = CotizacionDolar
        fields = ['fecha','valor']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date','class':'form-control'}),
            'valor': forms.NumberInput(attrs={'class':'form-control'}),
        }


class ConfiguracionIVAForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionIVA
        fields = ['fecha_inicio', 'porcentaje', 'activo']
        widgets = {
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date','class':'form-control'}),
            'porcentaje': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }