from django import forms
from ProveedoresApp.models import Proveedores

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = [
            'nombre',
            'contacto',
            'email',
            'telefono',
            'direccion',
            'rublo',
            'rif',
        ]   
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rublo': forms.TextInput(attrs={'class': 'form-control'}),
            'rif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: J-12345678-9'}),
        }