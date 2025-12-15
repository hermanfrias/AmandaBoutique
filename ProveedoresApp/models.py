from django.db import models
import uuid

# Create your models here.

def generar_code():
    return uuid.uuid4().hex

class Proveedores(models.Model):
    codigo_proveedor = models.CharField(
        max_length=32,
        unique=True,
        default=generar_code
    )
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    rublo = models.CharField(max_length=100)
    rif = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.nombre} - {self.rublo}"