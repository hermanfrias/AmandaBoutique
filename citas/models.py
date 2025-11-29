from django.db import models


from django.conf import settings

class Cita(models.Model):
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ACCIONES = [
        ('Medidas/Diseño', 'Medidas/Diseño'),
        ('Pruebas', 'Pruebas'),
        ('Entrega', 'Entrega'),
        ('Culminado', 'Culminado'),
        ('Cancelada', 'Cancelada'),
        ('Otros', 'Otros'),
    ]

    MONEDAS = [
        ('Bs', 'Bs'),
        ('$', '$'),
    ]

    cliente = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField(blank=True, null=True)
    copa = models.CharField(max_length=5, blank=True, null=True)  
    busto = models.CharField(max_length=5, blank=True, null=True)  
    cintura = models.CharField(max_length=5, blank=True, null=True) 
    largo = models.CharField(max_length=5, blank=True, null=True) 
    tiras = models.CharField(max_length=5, blank=True, null=True) 
    otra = models.CharField(max_length=50, blank=True, null=True)   
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # nuevo campo
    abono = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pago_total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    moneda = models.CharField(max_length=3, choices=MONEDAS, default='bs')  # nuevo campo
    accion = models.CharField(max_length=20, choices=ACCIONES, default='otros')
    fecha_entrega = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.cliente} - {self.fecha} {self.hora} ({self.get_accion_display()})"
   


