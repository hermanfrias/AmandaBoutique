from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CompraInsumo
from flujo.models import MovimientoCaja
import logging

logger = logging.getLogger(__name__)


# TEMPORALMENTE DESHABILITADO - Investigar por qué no se ejecuta
# @receiver(post_save, sender=CompraInsumo)
def crear_o_actualizar_movimiento_caja(sender, instance, created, **kwargs):
    """
    Crea o actualiza automáticamente un MovimientoCaja cuando se guarda una CompraInsumo.
    
    - Si es una compra nueva (created=True), crea un nuevo movimiento
    - Si es una edición (created=False), actualiza el movimiento existente
    """
    print(f"⚡ Signal ejecutado! CompraInsumo ID: {instance.pk}, Created: {created}")
    
    try:
        # Determinar el monto según la moneda
        if instance.moneda == 'Bs':
            monto = instance.monto_total_bs
        else:  # moneda == '$'
            monto = instance.monto_total_usd
        
        if created:
            # Crear nuevo movimiento para compra nueva
            try:
                print(f"🔍 Intentando crear MovimientoCaja:")
                print(f"   - Fecha: {instance.fecha_compra}")
                print(f"   - Moneda: {instance.moneda}")
                print(f"   - Monto: {monto}")
                
                MovimientoCaja.objects.create(
                    fecha=instance.fecha_compra,
                    descripcion='Compra insumos varios',
                    tipo='Gasto',
                    tipo_movimiento='Compra de Insumos',
                    metodo_pago='Efectivo',
                    moneda=instance.moneda,
                    monto=monto
                )
                print(f"✅ Movimiento de caja creado exitosamente para compra {instance.pk}")
                logger.info(f"Movimiento de caja creado para compra {instance.pk}")
            except Exception as e:
                error_msg = f"Error al crear movimiento de caja para compra {instance.pk}: {type(e).__name__}: {str(e)}"
                logger.error(error_msg)
                print(f"❌ {error_msg}")
                import traceback
                print(traceback.format_exc())
                # No lanzar la excepción para que la compra se guarde de todas formas
        else:
            # Actualizar movimiento existente para compra editada
            # Buscar el movimiento asociado a esta compra
            # Usamos la fecha y descripción para identificarlo
            try:
                movimiento = MovimientoCaja.objects.filter(
                    fecha=instance.fecha_compra,
                    descripcion='Compra insumos varios',
                    tipo='Gasto',
                    tipo_movimiento='Compra de Insumos'
                ).latest('id')  # Obtener el más reciente por si hay varios
                
                # Actualizar el movimiento
                movimiento.moneda = instance.moneda
                movimiento.monto = monto
                movimiento.save()
                logger.info(f"Movimiento de caja actualizado para compra {instance.pk}")
            except MovimientoCaja.DoesNotExist:
                # Si no existe el movimiento (por ejemplo, compra creada antes de implementar esto)
                # Crear uno nuevo
                try:
                    MovimientoCaja.objects.create(
                        fecha=instance.fecha_compra,
                        descripcion='Compra insumos varios',
                        tipo='Gasto',
                        tipo_movimiento='Compra de Insumos',
                        metodo_pago='Efectivo',
                        moneda=instance.moneda,
                        monto=monto
                    )
                    logger.info(f"Movimiento de caja creado para compra editada {instance.pk}")
                except Exception as e:
                    logger.error(f"Error al crear movimiento de caja para compra editada {instance.pk}: {str(e)}")
            except Exception as e:
                logger.error(f"Error al actualizar movimiento de caja para compra {instance.pk}: {str(e)}")
    except Exception as e:
        logger.error(f"Error general en signal de compra {instance.pk}: {str(e)}")
        # No lanzar la excepción para que la compra se guarde de todas formas
