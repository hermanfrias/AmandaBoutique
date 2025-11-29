from django import forms
from .models import MovimientoCaja, CotizacionDolar

class MovimientoCajaForm(forms.ModelForm):
    class Meta:
        model = MovimientoCaja
        fields = ['fecha', 'descripcion', 'tipo', 'moneda', 'monto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-select'}),
            'moneda': forms.Select(attrs={'class':'form-select'}),
            'monto': forms.NumberInput(attrs={'class':'form-control'}),
        }

class CotizacionDolarForm(forms.ModelForm):
    class Meta:
        model = CotizacionDolar
        fields = ['fecha','valor']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date','class':'form-control'}),
            'valor': forms.NumberInput(attrs={'class':'form-control'}),
        }