from django import forms
from .models import Catalogo

class CatalogoForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        exclude = ['codigo']
        fields = ['codigo','modelo', 'estilo', 'descripcion', 'precio', 'imagen_modelo', 'foto2', 'foto3', 'foto4']
        widgets = {
            "codigo": forms.TextInput(attrs={'class':'form-control'}),
            "modelo": forms.TextInput(attrs={'class':'form-control'}),
            "estilo": forms.TextInput(attrs={'class':'form-control'}),
            "descripcion": forms.TextInput(attrs={'class':'form-control'}),
            "precio": forms.NumberInput(attrs={'class':'form-control'}),
            "imagen_modelo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto2": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto3": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto4": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        
