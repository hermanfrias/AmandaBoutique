from django import forms
from .models import Cita


class CitaForm(forms.ModelForm):
    # Hacer los campos fecha y hora opcionales
    fecha = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={
            'type':'date',
            'class':'form-control',
            'required': False  # Evitar validación HTML5
        }, format='%Y-%m-%d')
    )
    hora = forms.TimeField(
        required=False, 
        widget=forms.TimeInput(attrs={
            'type':'time',
            'class':'form-control',
            'required': False  # Evitar validación HTML5
        })
    )
    
    class Meta:
        model = Cita
        fields = [
            'cliente', 'telefono', 'fecha','hora','descripcion','copa','busto', 'cintura','largo', 'tiras','otra', 'precio','abono','pago_total','moneda','accion', 'fecha_entrega'
        ]
        widgets = {
            'cliente': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_entrega': forms.DateInput(attrs={'type':'date','class':'form-control'}, format ='%Y-%m-%d'),
            'descripcion': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'copa': forms.TextInput(attrs={'class':'form-control'}),
            'busto': forms.TextInput(attrs={'class':'form-control'}),
            'cintura': forms.TextInput(attrs={'class':'form-control'}),
            'largo': forms.TextInput(attrs={'class':'form-control'}),
            'tiras': forms.TextInput(attrs={'class':'form-control'}),
            'otra': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'abono': forms.NumberInput(attrs={'class':'form-control'}),
            'pago_total': forms.NumberInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(attrs={'class':'form-select'}),
            'accion': forms.Select(attrs={'class':'form-select'}),
        }

