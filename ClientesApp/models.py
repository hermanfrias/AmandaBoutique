from django.db import models

# Create your models here.
class Clientes(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Campos de medidas (todos opcionales)
    copa = models.CharField(max_length=10, blank=True, null=True, verbose_name='Copa')
    busto = models.CharField(max_length=10, blank=True, null=True, verbose_name='Busto')
    cintura = models.CharField(max_length=10, blank=True, null=True, verbose_name='Cintura')
    largo = models.CharField(max_length=10, blank=True, null=True, verbose_name='Largo')
    tiras = models.CharField(max_length=10, blank=True, null=True, verbose_name='Tiras')
    otras = models.CharField(max_length=100, blank=True, null=True, verbose_name='Otras Medidas')
    
    # Campo historial
    historial = models.TextField(blank=True, null=True, verbose_name='Historial de Alquileres')

    def __str__(self):
        return f"{self.identificacion}: {self.apellido}, {self.nombre}"