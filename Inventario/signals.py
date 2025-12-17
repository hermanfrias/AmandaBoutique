from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import CompraInsumo
from flujo.models import MovimientoCaja
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=CompraInsumo)
def capturar_estado_anterior(sender, instance, **kwargs):
    """
    Captura el estado anterior de 'anulada' antes de guardar.
    Esto nos permite detectar si acabamos de anular en el post_save.
    """
    # Log a archivo
    with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"PRE_SAVE ejecutado para CompraInsumo ID: {instance.pk}\n")
        
    if instance.pk:  # Solo si ya existe en BD
        try:
            compra_anterior = CompraInsumo.objects.get(pk=instance.pk)
            instance._anulada_anterior = compra_anterior.anulada
            logger.info(f"PRE_SAVE: Capturado estado anterior anulada={compra_anterior.anulada} para compra {instance.pk}")
            with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                f.write(f"Estado anterior capturado: anulada={compra_anterior.anulada}\n")
        except CompraInsumo.DoesNotExist:
            instance._anulada_anterior = None
            with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                f.write(f"Compra no existe en BD\n")
    else:
        instance._anulada_anterior = None
        with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
            f.write(f"Compra nueva (sin PK)\n")


@receiver(post_save, sender=CompraInsumo)
def crear_o_actualizar_movimiento_caja(sender, instance, created, **kwargs):
    """
    Crea o actualiza automáticamente un MovimientoCaja cuando se guarda una CompraInsumo.
    
    IMPORTANTE: Este signal se ejecuta por cada CompraInsumo guardada. Cuando se crea una factura
    con múltiples ítems, se ejecutará múltiples veces. Para evitar crear múltiples movimientos,
    calculamos el total de TODAS las compras con el mismo numero_factura y fecha.
    
    - Si es una compra nueva (created=True), verifica si ya existe un movimiento para esa factura/fecha
      - Si NO existe, crea uno nuevo con el total de todas las compras de esa factura
      - Si YA existe, lo actualiza con el nuevo total
    - Si es una edición (created=False), actualiza el movimiento existente con el nuevo total
    """
    # Log a archivo PRIMERO
    try:
        with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"POST_SAVE INICIADO: ID={instance.pk}, Created={created}, Factura={instance.numero_factura}, Anulada={instance.anulada}\n")
    except Exception as e:
        pass  # Ignorar errores de log
    
    print(f"⚡ Signal ejecutado! CompraInsumo ID: {instance.pk}, Created: {created}, Factura: {instance.numero_factura}, Anulada: {instance.anulada}")
    logger.info(f"Signal ejecutado! CompraInsumo ID: {instance.pk}, Created: {created}, Factura: {instance.numero_factura}, Anulada: {instance.anulada}")
    
    try:
        # CASO ESPECIAL: Si la compra está siendo anulada, crear movimiento de reversa
        if instance.anulada and not created:
            # Verificar si acabamos de anular usando el estado anterior capturado en pre_save
            anulada_anterior = getattr(instance, '_anulada_anterior', None)
            
            logger.info(f"POST_SAVE: anulada_anterior={anulada_anterior}, anulada_actual={instance.anulada}")
            print(f"🔍 POST_SAVE: anulada_anterior={anulada_anterior}, anulada_actual={instance.anulada}")
            
            with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                f.write(f"Verificando anulación: anulada_anterior={anulada_anterior}, anulada_actual={instance.anulada}\n")
            
            # Si antes NO estaba anulada (False o None) y ahora SÍ está anulada (True)
            if anulada_anterior == False and instance.anulada == True:
                acabamos_de_anular = True
                logger.info(f"✅ ANULACIÓN DETECTADA: Cambió de False a True")
                print(f"✅ ANULACIÓN DETECTADA: Cambió de False a True")
                with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                    f.write(f"✅ ANULACIÓN DETECTADA! Creando reversa...\n")
            else:
                acabamos_de_anular = False
                logger.info(f"⏭️ No es una anulación nueva (anterior={anulada_anterior})")
                print(f"⏭️ No es una anulación nueva (anterior={anulada_anterior})")
                with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                    f.write(f"⏭️ No es anulación nueva (anterior={anulada_anterior})\n")
            
            if not acabamos_de_anular:
                return
            
            # Crear movimiento de reversa (Ingreso para compensar el Gasto original)
            print(f"🔄 Creando movimiento de REVERSA por anulación")
            logger.info(f"Creando movimiento de REVERSA")






            descripcion_reversa = f"REVERSA - Anulación Factura {instance.numero_factura}" if instance.numero_factura else "REVERSA - Anulación compra insumos"
            
            # Calcular monto de reversa
            if instance.moneda == 'Bs':
                monto_reversa = instance.monto_total_bs
            else:
                monto_reversa = instance.monto_total_usd
            
            try:
                with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                    f.write(f"Intentando crear MovimientoCaja...\n")
                    f.write(f"  Fecha: {instance.fecha_compra}\n")
                    f.write(f"  Descripción: {descripcion_reversa}\n")
                    f.write(f"  Monto: {monto_reversa} {instance.moneda}\n")
                
                MovimientoCaja.objects.create(
                    fecha=instance.fecha_compra,
                    descripcion=descripcion_reversa,
                    tipo='Ingreso',  # ← INGRESO para compensar el gasto
                    tipo_movimiento='Compra de Insumos',
                    metodo_pago='Efectivo',
                    moneda=instance.moneda,
                    monto=monto_reversa,
                    numero_factura=instance.numero_factura
                )
                
                with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                    f.write(f"✅ MovimientoCaja creado exitosamente!\n")
                
                print(f"✅ Movimiento de reversa creado: {monto_reversa} {instance.moneda}")
                logger.info(f"Movimiento de reversa creado por anulación de factura {instance.numero_factura}")
            except Exception as e:
                with open('e:/AmandaBoutique desarrollo/signal_debug.log', 'a', encoding='utf-8') as f:
                    f.write(f"❌ ERROR al crear MovimientoCaja: {str(e)}\n")
                logger.error(f"Error al crear movimiento de reversa: {str(e)}")
                
            return  # No continuar con la lógica normal
        
        # Si la compra está anulada (pero no acabamos de anularla), no crear/actualizar movimiento
        if instance.anulada:
            print(f"⏭️ Compra anulada, no se procesa movimiento")
            return
        

        # Obtener TODAS las compras con el mismo numero_factura y fecha
        # Esto asegura que el movimiento refleje el total de la factura completa
        if instance.numero_factura:
            compras_factura = CompraInsumo.objects.filter(
                numero_factura=instance.numero_factura,
                fecha_compra=instance.fecha_compra
            )
        else:
            # Si no tiene número de factura, solo considerar esta compra individual
            compras_factura = CompraInsumo.objects.filter(pk=instance.pk)
        
        # Calcular el total de la factura según la moneda
        if instance.moneda == 'Bs':
            monto_total = sum(c.monto_total_bs or 0 for c in compras_factura)
        else:  # moneda == '$'
            monto_total = sum(c.monto_total_usd or 0 for c in compras_factura)
        
        print(f"📊 Total de factura {instance.numero_factura}: {monto_total} {instance.moneda}")
        print(f"   Cantidad de ítems: {compras_factura.count()}")
        
        # Descripción del movimiento
        descripcion = f"Compra insumos - Factura {instance.numero_factura}" if instance.numero_factura else "Compra insumos varios"
        
        # Buscar movimiento existente usando numero_factura (más preciso)
        if instance.numero_factura:
            # Buscar por numero_factura (método preciso)
            movimiento_existente = MovimientoCaja.objects.filter(
                fecha=instance.fecha_compra,
                numero_factura=instance.numero_factura,
                tipo='Gasto',
                tipo_movimiento='Compra de Insumos'
            ).first()
            
            # Si no se encuentra, buscar por descripción (compatibilidad con movimientos antiguos)
            if not movimiento_existente:
                print(f"🔍 No se encontró por numero_factura, buscando por descripción (movimiento antiguo)...")
                movimiento_existente = MovimientoCaja.objects.filter(
                    fecha=instance.fecha_compra,
                    descripcion__in=[descripcion, "Compra insumos varios"],
                    tipo='Gasto',
                    tipo_movimiento='Compra de Insumos',
                    numero_factura__isnull=True  # Solo movimientos sin numero_factura
                ).first()
                
                # Si se encuentra, actualizar con el numero_factura
                if movimiento_existente:
                    print(f"✏️ Actualizando movimiento antiguo con numero_factura")
                    movimiento_existente.numero_factura = instance.numero_factura
                    movimiento_existente.descripcion = descripcion
        else:
            # Para compras sin numero_factura, buscar por descripción
            movimiento_existente = MovimientoCaja.objects.filter(
                fecha=instance.fecha_compra,
                descripcion="Compra insumos varios",
                tipo='Gasto',
                tipo_movimiento='Compra de Insumos',
                numero_factura__isnull=True
            ).first()
        
        if movimiento_existente:
            # Actualizar el movimiento existente con el nuevo total
            print(f"🔄 Actualizando movimiento existente ID: {movimiento_existente.pk}")
            movimiento_existente.moneda = instance.moneda
            movimiento_existente.monto = monto_total
            movimiento_existente.save()
            print(f"✅ Movimiento actualizado con total: {monto_total} {instance.moneda}")
            logger.info(f"Movimiento de caja actualizado para factura {instance.numero_factura}: {monto_total} {instance.moneda}")
        else:
            # Crear nuevo movimiento
            print(f"🆕 Creando nuevo movimiento de caja")
            MovimientoCaja.objects.create(
                fecha=instance.fecha_compra,
                descripcion=descripcion,
                tipo='Gasto',
                tipo_movimiento='Compra de Insumos',
                metodo_pago='Efectivo',
                moneda=instance.moneda,
                monto=monto_total,
                numero_factura=instance.numero_factura  # ← NUEVO CAMPO
            )
            print(f"✅ Movimiento de caja creado con total: {monto_total} {instance.moneda}")
            logger.info(f"Movimiento de caja creado para factura {instance.numero_factura}: {monto_total} {instance.moneda}")
            
    except Exception as e:
        error_msg = f"Error en signal para compra {instance.pk}: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        import traceback
        print(traceback.format_exc())
        # No lanzar la excepción para que la compra se guarde de todas formas
