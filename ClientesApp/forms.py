from django import forms
from ClientesApp.models import Clientes

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'identificacion', 'nombre', 'apellido', 'email', 'telefono', 'direccion',
            'copa', 'busto', 'cintura', 'largo', 'tiras', 'otras', 'historial'
        ]
        widgets = {
            "identificacion": forms.TextInput(attrs={'class':'form-control'}),
            "nombre": forms.TextInput(attrs={'class':'form-control'}),
            "apellido": forms.TextInput(attrs={'class':'form-control'}),
            "email": forms.EmailInput(attrs={'class':'form-control'}),
            "telefono": forms.TextInput(attrs={'class':'form-control'}), 
            "direccion": forms.Textarea(attrs={'class':'form-control', 'rows': 2}),
            # Campos de medidas
            "copa": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ej: 34B'}),
            "busto": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ej: 90cm'}),
            "cintura": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ej: 70cm'}),
            "largo": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ej: 150cm'}),
            "tiras": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ej: 40cm'}),
            "otras": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Otras medidas'}),
            # Campo historial
            "historial": forms.Textarea(attrs={'class':'form-control', 'rows': 3, 'placeholder': 'Notas sobre alquileres anteriores'}),
        }
