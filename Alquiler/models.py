from django.db import models
from ClientesApp.models import Clientes
from django.core.exceptions import ValidationError
from decimal import Decimal


class Vestido(models.Model):
    """Modelo para gestionar el inventario de vestidos disponibles para alquiler"""
    
    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Alquilado', 'Alquilado'),
        ('Tintorería', 'Tintorería'),
        ('Arreglo', 'Arreglo'),
        ('Dañado', 'Dañado'),
        ('Vendido', 'Vendido'),
        ('Baja', 'Baja'),
    ]
    
    MONEDAS = [
        ('Bs', 'Bolívares'),
        ('$', 'Dólares'),
    ]
    
    # Campos principales
    nombre_modelo = models.CharField(max_length=200, verbose_name='Nombre/Modelo')
    descripcion = models.TextField(verbose_name='Descripción')
    talla = models.CharField(max_length=20, verbose_name='Talla')
    color = models.CharField(max_length=50, verbose_name='Color')
    
    # Precios
    precio_alquiler = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de Alquiler')
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor de Compra')
    deposito_garantia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Depósito de Garantía', default=0)
    
    # Estado y disponibilidad
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Disponible', verbose_name='Estado')
    
    # Fotos
    foto1 = models.ImageField(upload_to='vestidos/', verbose_name='Foto 1')
    foto2 = models.ImageField(upload_to='vestidos/', blank=True, null=True, verbose_name='Foto 2')
    foto3 = models.ImageField(upload_to='vestidos/', blank=True, null=True, verbose_name='Foto 3')
    foto4 = models.ImageField(upload_to='vestidos/', blank=True, null=True, verbose_name='Foto 4')
    
    # Información adicional
    accesorios = models.TextField(blank=True, null=True, verbose_name='Accesorios Incluidos')

    
    # Tintorería
    fecha_tintoreria = models.DateField(blank=True, null=True, verbose_name='Fecha de Envío a Tintorería')
    fecha_entrega_tintoreria = models.DateField(blank=True, null=True, verbose_name='Fecha de Entrega de Tintorería')
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Vestido'
        verbose_name_plural = 'Vestidos'
    
    def __str__(self):
        return f"{self.nombre_modelo} - {self.talla} - {self.color}"
    
    def esta_disponible(self):
        """Verifica si el vestido está disponible para alquilar"""
        return self.estado == 'Disponible'


class Alquiler(models.Model):
    """Modelo para gestionar las transacciones de alquiler de vestidos"""
    
    ESTADO_PAGO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('Parcial', 'Parcial'),
    ]
    
    ESTADO_ALQUILER_CHOICES = [
        ('Activo', 'Activo'),
        ('Entregado', 'Entregado'),
        ('Devuelto', 'Devuelto'),
        ('Retrasado', 'Retrasado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    MONEDAS = [
        ('Bs', 'Bolívares'),
        ('$', 'Dólares'),
    ]
    
    # Relaciones
    cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT, related_name='alquileres', verbose_name='Cliente')
    vestido = models.ForeignKey(Vestido, on_delete=models.PROTECT, related_name='alquileres', verbose_name='Vestido')
    
    # Fechas
    fecha_contrato = models.DateField(verbose_name='Fecha de Contrato')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_devolucion_prevista = models.DateField(verbose_name='Fecha de Devolución Prevista')
    fecha_devolucion_real = models.DateField(blank=True, null=True, verbose_name='Fecha de Devolución Real')
    
    # Montos
    tipo_moneda = models.CharField(max_length=2, choices=MONEDAS, default='$', verbose_name='Tipo de Moneda')
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Anticipo')
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Final')
    deposito = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Depósito')
    pago_final = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Pago Final/Liquidación', default=0)
    pago_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name='Pago Total Recibido', default=0)
    total_usd = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name='Total en USD', default=0)
    pago_total_usd = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name='Pago Total en USD', default=0)
    
    # Estados
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='Pendiente', verbose_name='Estado de Pago')
    estado_alquiler = models.CharField(max_length=20, choices=ESTADO_ALQUILER_CHOICES, default='Activo', verbose_name='Estado del Alquiler')
    
    # Notas
    notas = models.TextField(blank=True, null=True, verbose_name='Notas')
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_contrato']
        verbose_name = 'Alquiler'
        verbose_name_plural = 'Alquileres'
    
    def clean(self):
        """Validaciones personalizadas"""
        # Validar que fecha_devolucion_prevista sea posterior a fecha_inicio
        if self.fecha_devolucion_prevista and self.fecha_inicio:
            if self.fecha_devolucion_prevista <= self.fecha_inicio:
                raise ValidationError({
                    'fecha_devolucion_prevista': 'La fecha de devolución prevista debe ser posterior a la fecha de inicio.'
                })
        
        # Validar que anticipo no sea mayor que monto_final
        if self.anticipo and self.monto_final:
            if self.anticipo > self.monto_final:
                raise ValidationError({
                    'anticipo': 'El anticipo no puede ser mayor que el monto final.'
                })
        
        # Validar que el vestido esté disponible (solo para nuevos alquileres)
        if not self.pk and self.vestido:
            if not self.vestido.esta_disponible():
                raise ValidationError({
                    'vestido': f'El vestido "{self.vestido}" no está disponible para alquilar. Estado actual: {self.vestido.estado}'
                })
    
    def save(self, *args, **kwargs):
        # Ejecutar validaciones
        self.full_clean()
        
        # Obtener la tasa de cambio
        try:
            from flujo.models import ConfiguracionIVA
            config = ConfiguracionIVA.objects.latest('fecha_vigencia')
            tasa_cambio = config.tasa_cambio if hasattr(config, 'tasa_cambio') else Decimal('36.50')
        except:
            # Valor por defecto si no hay configuración
            tasa_cambio = Decimal('36.50')
        
        # Calcular pago_total como anticipo + pago_final
        self.pago_total = self.anticipo + self.pago_final
        
        # Calcular total_usd basado en tipo_moneda
        if self.tipo_moneda == 'Bs':
            # Convertir el monto total (monto_final + deposito) a USD
            total_bs = self.monto_final + self.deposito
            self.total_usd = total_bs / tasa_cambio
            # Convertir pago_total a USD
            self.pago_total_usd = self.pago_total / tasa_cambio
        else:
            # Si ya está en dólares, el total es la suma directa
            self.total_usd = self.monto_final + self.deposito
            self.pago_total_usd = self.pago_total
        
        # Obtener el estado anterior del alquiler si existe
        estado_anterior = None
        if self.pk:
            try:
                estado_anterior = Alquiler.objects.get(pk=self.pk).estado_alquiler
            except Alquiler.DoesNotExist:
                pass
        
        # Si es un nuevo alquiler, cambiar el estado del vestido a "Alquilado"
        if not self.pk and self.vestido.esta_disponible():
            self.vestido.estado = 'Alquilado'
            self.vestido.save()
        
        # Si el estado del alquiler cambió, actualizar el estado del vestido
        elif self.pk and estado_anterior and estado_anterior != self.estado_alquiler:
            # Cuando el alquiler se cancela, el vestido vuelve a estar disponible
            if self.estado_alquiler == 'Cancelado':
                self.vestido.estado = 'Disponible'
                self.vestido.save()
            # Cuando el alquiler se devuelve, el vestido va a tintorería
            elif self.estado_alquiler == 'Devuelto':
                self.vestido.estado = 'Tintorería'
                self.vestido.save()
        
        super().save(*args, **kwargs)
    
    def calcular_saldo_pendiente(self):
        """Calcula el saldo pendiente de pago (monto_final + deposito - pago_total)"""
        total_a_pagar = self.monto_final + self.deposito
        return total_a_pagar - self.pago_total
    
    def marcar_como_devuelto(self, fecha_devolucion=None):
        """Marca el alquiler como completado y libera el vestido"""
        from datetime import date
        
        self.fecha_devolucion_real = fecha_devolucion or date.today()
        self.estado_alquiler = 'Completado'
        
        # Liberar el vestido
        self.vestido.estado = 'Disponible'
        self.vestido.save()
        
        self.save()
    
    def __str__(self):
        return f"Alquiler #{self.pk} - {self.cliente.nombre} {self.cliente.apellido} - {self.vestido.nombre_modelo}"

# ============================================
# SIGNALS PARA ELIMINAR FOTOS AUTOMÁTICAMENTE
# ============================================

import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

@receiver(post_delete, sender=Vestido)
def auto_delete_vestido_photos_on_delete(sender, instance, **kwargs):
    '''Elimina las fotos del sistema de archivos cuando se elimina un Vestido'''
    for field_name in ['foto1', 'foto2', 'foto3', 'foto4']:
        field = getattr(instance, field_name)
        if field:
            if os.path.isfile(field.path):
                try:
                    os.remove(field.path)
                except Exception as e:
                    print(f'Error al eliminar {field_name}: {e}')

@receiver(pre_save, sender=Vestido)
def auto_delete_vestido_photos_on_change(sender, instance, **kwargs):
    '''Elimina la foto antigua cuando se reemplaza por una nueva'''
    if not instance.pk:
        return False

    try:
        old_instance = Vestido.objects.get(pk=instance.pk)
    except Vestido.DoesNotExist:
        return False

    for field_name in ['foto1', 'foto2', 'foto3', 'foto4']:
        old_field = getattr(old_instance, field_name)
        new_field = getattr(instance, field_name)
        
        if old_field and old_field != new_field:
            if os.path.isfile(old_field.path):
                try:
                    os.remove(old_field.path)
                except Exception as e:
                    print(f'Error al eliminar {field_name} antigua: {e}')
