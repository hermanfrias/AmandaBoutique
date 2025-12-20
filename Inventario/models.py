from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from ProveedoresApp.models import Proveedores


class ExistenciaInsumo(models.Model):
    MEDIDAS = [
        ('Unidades', 'Unidades'),
        ('Metros', 'Metros'),
    ]
    CATEGORIA_CHOICES = [
        ('Telas', 'Telas'),
        ('Hilos', 'Hilos'),
        ('Adornos', 'Adornos'),
        ('Estructura', 'Estructura'),
        ('Otros', 'Otros'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=150, unique=True)
    medida = models.CharField(max_length=20, choices=MEDIDAS)
    existencia = models.DecimalField(max_digits=10, decimal_places=2)
    existencia_minima = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Existencia mínima requerida")
    costo_dolar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Costo unitario en USD (se calcula automáticamente al registrar compras)")
    proveedor = models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True, blank=True, related_name='insumos')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='Otros')

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Generar código automático INS + 4 dígitos
            while True:
                try:
                    ultimo = ExistenciaInsumo.objects.all().order_by('codigo').last()
                    if not ultimo:
                        nuevo_codigo = 'INS0001'
                    else:
                        try:
                            num = int(ultimo.codigo.replace('INS', '')) + 1
                        except ValueError:
                            num = 1
                        nuevo_codigo = f"INS{num:04d}"
                    
                    self.codigo = nuevo_codigo
                    super().save(*args, **kwargs)
                    break
                except Exception as e:
                    if 'unique constraint' in str(e).lower() or 'integrity' in str(e).lower():
                        continue
                    raise e
        else:
            super().save(*args, **kwargs)

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Existencia de Insumo'
        verbose_name_plural = 'Existencias de Insumos'

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class CompraInsumo(models.Model):
    MONEDAS = [
        ('Bs', 'Bolívares'),
        ('$', 'Dólares'),
    ]
    
    insumo = models.ForeignKey(ExistenciaInsumo, on_delete=models.CASCADE, related_name='compras')
    numero_factura = models.CharField(max_length=50, blank=True, null=True, verbose_name='Número de Factura')
    fecha_compra = models.DateField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=2, choices=MONEDAS)
    monto = models.DecimalField(max_digits=15, decimal_places=2, help_text="Monto en la moneda seleccionada")
    aplicar_iva = models.BooleanField(default=False, verbose_name="Aplicar IVA (16%)")
    
    # Campos calculados automáticamente
    monto_bs = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, editable=False)
    monto_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, editable=False)
    monto_iva_bs = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, editable=False)
    monto_iva_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, editable=False)
    monto_total_bs = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, editable=False)
    monto_total_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, editable=False)
    
    # Campos de anulación
    anulada = models.BooleanField(default=False, verbose_name='Anulada', help_text='Indica si esta compra ha sido anulada')
    fecha_anulacion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Anulación')

    class Meta:
        ordering = ['-fecha_compra']
        verbose_name = 'Compra de Insumo'
        verbose_name_plural = 'Compras de Insumos'

    def clean(self):
        # Validar que existe cotización para la fecha de compra
        from flujo.models import CotizacionDolar
        if not CotizacionDolar.objects.filter(fecha=self.fecha_compra).exists():
            raise ValidationError(
                f'No existe cotización del dólar para la fecha {self.fecha_compra.strftime("%d/%m/%Y")}. '
                'Por favor registre la cotización del día primero.'
            )
    
    def anular(self):
        """Anula esta compra, revierte inventario y marca como anulada"""
        from django.utils import timezone
        
        if self.anulada:
            raise ValidationError('Esta compra ya está anulada')
        
        # Marcar como anulada
        self.anulada = True
        self.fecha_anulacion = timezone.now()
        
        print(f"🔴 ANULAR: Iniciando anulación de compra ID: {self.pk}")
        print(f"   Factura: {self.numero_factura}")
        print(f"   Insumo: {self.insumo.codigo}")
        
        # Revertir inventario (restar la cantidad que se había sumado)
        self.insumo.existencia -= self.cantidad
        self.insumo.save()
        print(f"   ✅ Inventario revertido")
        
        # Marcar que acabamos de anular (para que el signal lo detecte)
        self._acabamos_de_anular = True
        
        # Guardar (el signal creará el movimiento de reversa)
        print(f"   💾 Guardando compra anulada...")
        self.save()
        print(f"   ✅ Compra guardada. Anulada={self.anulada}, Fecha={self.fecha_anulacion}")



    def save(self, *args, **kwargs):
        from flujo.models import CotizacionDolar
        
        # Ejecutar validaciones
        self.full_clean()
        
        # Obtener cotización del día
        try:
            cotizacion = CotizacionDolar.objects.get(fecha=self.fecha_compra)
        except CotizacionDolar.DoesNotExist:
            raise ValidationError(
                f'No existe cotización del dólar para la fecha {self.fecha_compra.strftime("%d/%m/%Y")}.'
            )
        
        # Calcular montos según la moneda seleccionada
        if self.moneda == 'Bs':
            self.monto_bs = self.monto
            self.monto_usd = Decimal(self.monto) / cotizacion.valor
        else:  # moneda == '$'
            self.monto_usd = self.monto
            self.monto_bs = Decimal(self.monto) * cotizacion.valor
        
        # Calcular IVA si aplica
        if self.aplicar_iva:
            # Obtener IVA dinámico según la fecha de compra
            from flujo.models import ConfiguracionIVA
            iva_rate = ConfiguracionIVA.obtener_iva_para_fecha(self.fecha_compra)
            self.monto_iva_bs = self.monto_bs * iva_rate
            self.monto_iva_usd = self.monto_usd * iva_rate
            self.monto_total_bs = self.monto_bs + self.monto_iva_bs
            self.monto_total_usd = self.monto_usd + self.monto_iva_usd
        else:
            self.monto_iva_bs = Decimal('0')
            self.monto_iva_usd = Decimal('0')
            self.monto_total_bs = self.monto_bs
            self.monto_total_usd = self.monto_usd
        
        # Guardar la cantidad anterior si es una edición
        cantidad_anterior = Decimal('0')
        if self.pk:  # Si ya existe (es una edición)
            try:
                compra_anterior = CompraInsumo.objects.get(pk=self.pk)
                cantidad_anterior = compra_anterior.cantidad
            except CompraInsumo.DoesNotExist:
                cantidad_anterior = Decimal('0')
        
        print(f"💾 CompraInsumo.save() llamado - PK antes: {self.pk}")
        super().save(*args, **kwargs)
        print(f"💾 CompraInsumo.save() completado - PK después: {self.pk}")
        
        # Actualizar el insumo automáticamente
        if self.cantidad > 0:
            # Calcular la diferencia de cantidad
            diferencia_cantidad = self.cantidad - cantidad_anterior
            
            # Actualizar existencia: ajustar según la diferencia
            self.insumo.existencia += diferencia_cantidad
            
            # Actualizar costo_dolar: calcular monto_total_usd / cantidad
            nuevo_costo = self.monto_total_usd / self.cantidad
            self.insumo.costo_dolar = nuevo_costo
            
            self.insumo.save()

    def __str__(self):
        return f"{self.fecha_compra.strftime('%d/%m/%Y')} - {self.insumo.codigo} - {self.cantidad} {self.insumo.medida}"


class UsoInsumo(models.Model):
    fecha_uso = models.DateField(verbose_name="Fecha de Uso")
    descripcion = models.CharField(max_length=300, verbose_name="Descripción del Uso")
    costo_total_usd = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False, verbose_name="Costo Total (USD)")
    
    class Meta:
        ordering = ['-fecha_uso']
        verbose_name = 'Uso de Insumo'
        verbose_name_plural = 'Usos de Insumos'
    
    def calcular_costo_total(self):
        """Calcula el costo total sumando todos los detalles"""
        total = sum(detalle.costo_total_usd for detalle in self.detalles.all())
        # Usar update para evitar recursión con save()
        UsoInsumo.objects.filter(pk=self.pk).update(costo_total_usd=total)
    
    def __str__(self):
        return f"{self.fecha_uso.strftime('%d/%m/%Y')} - {self.descripcion}"


class DetalleUsoInsumo(models.Model):
    uso = models.ForeignKey(UsoInsumo, on_delete=models.CASCADE, related_name='detalles')
    insumo = models.ForeignKey(ExistenciaInsumo, on_delete=models.PROTECT, related_name='usos')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Utilizada")
    costo_unitario_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Unitario (USD)")
    costo_total_usd = models.DecimalField(max_digits=15, decimal_places=2, editable=False, verbose_name="Costo Total (USD)")
    
    class Meta:
        verbose_name = 'Detalle de Uso'
        verbose_name_plural = 'Detalles de Uso'
    
    def clean(self):
        # Las validaciones de existencia y costo se manejan en save()
        # para tener acceso al pk y poder diferenciar entre creación y edición
        pass

    
    def save(self, *args, **kwargs):
        # Establecer costo_unitario_usd ANTES de la validación si es nuevo
        if not self.pk and not self.costo_unitario_usd:
            if not self.insumo.costo_dolar:
                raise ValidationError(
                    f'El insumo {self.insumo.descripcion} no tiene costo unitario definido. '
                    'Por favor registre una compra primero.'
                )
            self.costo_unitario_usd = self.insumo.costo_dolar
        
        # Calcular costo total
        if self.cantidad and self.costo_unitario_usd:
            self.costo_total_usd = self.cantidad * self.costo_unitario_usd
        
        # Ejecutar validaciones
        self.full_clean()
        
        # Manejar actualización de existencia
        if self.pk:
            # Es una edición - obtener el detalle anterior
            detalle_anterior = DetalleUsoInsumo.objects.get(pk=self.pk)
            diferencia = self.cantidad - detalle_anterior.cantidad
            
            # Validar que hay existencia suficiente para la diferencia
            if diferencia > 0 and diferencia > self.insumo.existencia:
                raise ValidationError(
                    f'No hay suficiente existencia de {self.insumo.descripcion}. '
                    f'Disponible: {self.insumo.existencia} {self.insumo.medida}, '
                    f'Adicional requerido: {diferencia} {self.insumo.medida}'
                )
            
            # Ajustar existencia según la diferencia
            self.insumo.existencia -= diferencia
            self.insumo.save()
        else:
            # Es un nuevo registro - validar existencia
            if self.cantidad > self.insumo.existencia:
                raise ValidationError(
                    f'No hay suficiente existencia de {self.insumo.descripcion}. '
                    f'Disponible: {self.insumo.existencia} {self.insumo.medida}, '
                    f'Solicitado: {self.cantidad} {self.insumo.medida}'
                )
            
            # Restar de la existencia
            self.insumo.existencia -= self.cantidad
            self.insumo.save()
        
        super().save(*args, **kwargs)
        
        # Actualizar el costo total del uso
        if hasattr(self, 'uso') and self.uso:
            self.uso.calcular_costo_total()

    
    def delete(self, *args, **kwargs):
        # Restaurar la existencia al eliminar
        self.insumo.existencia += self.cantidad
        self.insumo.save()
        
        super().delete(*args, **kwargs)
        
        # Actualizar el costo total del uso
        self.uso.calcular_costo_total()
    
    def __str__(self):
        return f"{self.insumo.codigo} - {self.cantidad} {self.insumo.medida}"


# ============================================
# MODELO: ACTIVO FIJO
# ============================================

class ActivoFijo(models.Model):
    TIPO_ACTIVO_CHOICES = [
        ('Maquinaria', 'Maquinaria'),
        ('Herramienta', 'Herramienta'),
        ('Mobiliario', 'Mobiliario'),
        ('Equipo de Oficina', 'Equipo de Oficina'),
        ('Vehículo', 'Vehículo'),        
        ('Tecnología', 'Tecnología'),
        ('Otros', 'Otros'),
    ]
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('En Mantenimiento', 'En Mantenimiento'),
        ('Dado de Baja', 'Dado de Baja'),
        ('Vendido', 'Vendido'),
    ]
    
    MONEDAS = [
        ('Bs', 'Bolívares'),
        ('$', 'Dólares'),
    ]
    
    # Campos principales
    numero_inventario = models.CharField(max_length=20, unique=True, blank=True, verbose_name='Número de Inventario')
    descripcion_corta = models.CharField(max_length=200, blank=True, null=True, verbose_name='Descripción Corta')
    fecha_adquisicion = models.DateField(verbose_name='Fecha de Adquisición')
    tipo_activo = models.CharField(max_length=50, choices=TIPO_ACTIVO_CHOICES, verbose_name='Tipo de Activo')
    marca = models.CharField(max_length=100, blank=True, null=True, verbose_name='Marca')
    modelo = models.CharField(max_length=100, blank=True, null=True, verbose_name='Modelo')
    serial = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='Serial')
    proveedor = models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True, blank=True, related_name='activos_fijos', verbose_name='Proveedor')
    
    # Valores monetarios
    moneda = models.CharField(max_length=2, choices=MONEDAS, verbose_name='Moneda')
    valor_adquisicion = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor de Adquisición')
    valor_dolares = models.DecimalField(max_digits=15, decimal_places=2, editable=False, verbose_name='Valor en Dólares')
    
    # Depreciación
    depreciacion_anual = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Depreciación Anual (%)', help_text='Porcentaje de depreciación anual (ej: 20.00 para 20%)')
    depreciacion_acumulada = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False, verbose_name='Depreciación Acumulada (USD)')
    valor_actual = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False, verbose_name='Valor Actual (USD)')
    
    # Estado y ubicación
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', verbose_name='Estado')
    ubicacion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Ubicación')
    responsable = models.CharField(max_length=200, blank=True, null=True, verbose_name='Responsable')
    
    # Mantenimiento
    fecha_mantenimiento = models.DateField(blank=True, null=True, verbose_name='Última Fecha de Mantenimiento')
    descripcion_mantenimiento = models.TextField(blank=True, null=True, verbose_name='Descripción del Mantenimiento')
    
    # Garantía
    garantia_meses = models.IntegerField(default=0, verbose_name='Garantía (meses)', help_text='Duración de la garantía en meses desde la fecha de adquisición')
    
    # Información adicional
    foto = models.ImageField(upload_to='activos_fijos/', blank=True, null=True, verbose_name='Foto del Activo')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        ordering = ['-fecha_adquisicion', 'numero_inventario']
        verbose_name = 'Activo Fijo'
        verbose_name_plural = 'Activos Fijos'
    
    def save(self, *args, **kwargs):
        # Auto-generar numero_inventario
        if not self.numero_inventario:
            ultimo = ActivoFijo.objects.order_by('-numero_inventario').first()
            if ultimo and ultimo.numero_inventario.startswith('AF'):
                try:
                    numero = int(ultimo.numero_inventario[2:]) + 1
                    self.numero_inventario = f'AF{numero:05d}'
                except ValueError:
                    self.numero_inventario = 'AF00001'
            else:
                self.numero_inventario = 'AF00001'
        
        # Calcular valor en dólares si la compra fue en Bs
        if self.moneda == 'Bs':
            from flujo.models import CotizacionDolar
            try:
                cotizacion = CotizacionDolar.objects.filter(
                    fecha=self.fecha_adquisicion
                ).first()
                if cotizacion:
                    self.valor_dolares = self.valor_adquisicion / cotizacion.valor
                else:
                    # Si no hay cotización para esa fecha, usar la más reciente
                    cotizacion_reciente = CotizacionDolar.objects.order_by('-fecha').first()
                    if cotizacion_reciente:
                        self.valor_dolares = self.valor_adquisicion / cotizacion_reciente.valor
                    else:
                        self.valor_dolares = Decimal('0')
            except Exception:
                self.valor_dolares = Decimal('0')
        else:
            # Si la compra fue en dólares, valor_dolares = valor_adquisicion
            self.valor_dolares = self.valor_adquisicion
        
        # Calcular depreciación acumulada
        self.calcular_depreciacion()
        
        super().save(*args, **kwargs)
    
    def calcular_depreciacion(self):
        """Calcula la depreciación acumulada basada en años transcurridos"""
        from datetime import date
        
        if self.fecha_adquisicion and self.valor_dolares and self.depreciacion_anual:
            años_transcurridos = (date.today() - self.fecha_adquisicion).days / Decimal('365.25')
            # Depreciación se calcula sobre el valor en dólares
            depreciacion_anual_monto = (self.valor_dolares * self.depreciacion_anual) / Decimal('100')
            self.depreciacion_acumulada = min(
                depreciacion_anual_monto * Decimal(str(años_transcurridos)),
                self.valor_dolares  # No puede depreciar más del valor original
            )
            self.valor_actual = self.valor_dolares - self.depreciacion_acumulada
        else:
            self.depreciacion_acumulada = Decimal('0')
            self.valor_actual = self.valor_dolares if self.valor_dolares else Decimal('0')
    
    def get_vida_util_restante(self):
        """Retorna años de vida útil restante"""
        from datetime import date
        
        if self.depreciacion_anual > 0:
            vida_util_total = Decimal('100') / self.depreciacion_anual
            años_transcurridos = (date.today() - self.fecha_adquisicion).days / Decimal('365.25')
            return max(Decimal('0'), vida_util_total - Decimal(str(años_transcurridos)))
        return Decimal('0')
    
    def get_porcentaje_depreciacion(self):
        """Retorna el porcentaje de depreciación acumulada"""
        if self.valor_dolares > 0:
            return (self.depreciacion_acumulada / self.valor_dolares) * Decimal('100')
        return Decimal('0')
    
    def get_fecha_expiracion_garantia(self):
        """Retorna la fecha de expiración de la garantía"""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        if self.fecha_adquisicion and self.garantia_meses > 0:
            return self.fecha_adquisicion + relativedelta(months=self.garantia_meses)
        return None
    
    def garantia_vigente(self):
        """Retorna True si la garantía está vigente"""
        from datetime import date
        
        fecha_expiracion = self.get_fecha_expiracion_garantia()
        if fecha_expiracion:
            return date.today() <= fecha_expiracion
        return False
    
    def dias_restantes_garantia(self):
        """Retorna los días restantes de garantía (negativo si ya expiró)"""
        from datetime import date
        
        fecha_expiracion = self.get_fecha_expiracion_garantia()
        if fecha_expiracion:
            return (fecha_expiracion - date.today()).days
        return None
    
    def __str__(self):
        return f"{self.numero_inventario} - {self.tipo_activo} - {self.marca or ''} {self.modelo or ''}".strip()
