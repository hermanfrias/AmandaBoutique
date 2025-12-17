from django.db import models
from django.core.exceptions import ValidationError

class CotizacionDolar(models.Model):
    fecha = models.DateField(unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Bs por USD
    class Meta:
        ordering = ['-fecha']
    def __str__(self):
        return f"{self.fecha} - {self.valor} Bs"

class MovimientoCaja(models.Model):
    MONEDAS = [('Bs','Bolívares'),('$','Dólares')]
    TIPO = [('Ingreso','Ingreso'),('Gasto','Gasto')]
    TIPO_MOVIMIENTO = [
        ('Venta', 'Venta'),
        ('Compra de Insumos', 'Compra de Insumos'),
        ('Nómina', 'Nómina'),
        ('Alquiler', 'Alquiler'),
        ('Otros', 'Otros')
    ]
    METODO_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Depósito', 'Depósito'),
        ('Transferencia', 'Transferencia'),
        ('Pago Móvil', 'Pago Móvil'),
        ('Otro', 'Otro')
    ]
    
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    moneda = models.CharField(max_length=2, choices=MONEDAS, default='Bs')
    monto_usd = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO, blank=True, null=True)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO, blank=True, null=True)
    numero_factura = models.CharField(max_length=50, blank=True, null=True, verbose_name='Número de Factura', help_text='Número de factura asociado (para compras de insumos)')



    class Meta:
        ordering = ['-fecha']

    def clean(self):
        # Validamos que exista la cotización antes de guardar
        if self.moneda == 'Bs':
            if not CotizacionDolar.objects.filter(fecha=self.fecha).exists():
                raise ValidationError('No existe cotización para la fecha de este movimiento. Por favor registre la cotización del día primero.')

    def save(self, *args, **kwargs):
        from decimal import Decimal
        self.full_clean() # Ejecuta clean() antes de guardar
        if self.moneda == 'Bs':
            # Ya validamos en clean() que existe, pero por seguridad en save() directo:
            try:
                cot = CotizacionDolar.objects.get(fecha=self.fecha)
                self.monto_usd = Decimal(self.monto) / cot.valor
            except CotizacionDolar.DoesNotExist:
                 # Esto no debería pasar si se llama a clean(), pero por si acaso
                 raise ValidationError('No existe cotización para la fecha de este movimiento.')
        else:
            self.monto_usd = self.monto
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.fecha} - {self.tipo} - {self.monto} {self.moneda} / {self.monto_usd} $'