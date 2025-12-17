from django.core.management.base import BaseCommand
from Inventario.models import CompraInsumo
from flujo.models import MovimientoCaja


class Command(BaseCommand):
    help = 'Revierte la anulación de una factura específica'

    def add_arguments(self, parser):
        parser.add_argument('numero_factura', type=str, help='Número de factura a reactivar')

    def handle(self, *args, **options):
        numero_factura = options['numero_factura']
        
        # Buscar todas las compras de la factura
        compras = CompraInsumo.objects.filter(numero_factura=numero_factura, anulada=True)

        if not compras.exists():
            self.stdout.write(self.style.ERROR(f'No se encontraron compras anuladas para la factura {numero_factura}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Encontradas {compras.count()} compras anuladas para la factura {numero_factura}'))
        
        # Revertir cada compra
        for compra in compras:
            self.stdout.write(f'\n📦 Procesando: {compra.insumo.codigo} - {compra.insumo.descripcion}')
            self.stdout.write(f'   Cantidad: {compra.cantidad}')
            
            # Restaurar inventario (sumar la cantidad de nuevo)
            compra.insumo.existencia += compra.cantidad
            compra.insumo.save()
            self.stdout.write(self.style.SUCCESS(f'   ✅ Inventario restaurado: {compra.insumo.existencia}'))
            
            # Marcar como NO anulada
            compra.anulada = False
            compra.fecha_anulacion = None
            compra.save()
            self.stdout.write(self.style.SUCCESS(f'   ✅ Compra marcada como activa'))
        
        # Buscar y eliminar el movimiento de reversa
        movimientos_reversa = MovimientoCaja.objects.filter(
            numero_factura=numero_factura,
            descripcion__icontains="REVERSA"
        )
        
        if movimientos_reversa.exists():
            self.stdout.write(f'\n🔄 Encontrados {movimientos_reversa.count()} movimiento(s) de reversa')
            for mov in movimientos_reversa:
                self.stdout.write(f'   Eliminando: {mov.descripcion} - {mov.monto} {mov.moneda}')
                mov.delete()
            self.stdout.write(self.style.SUCCESS(f'   ✅ Movimiento(s) de reversa eliminado(s)'))
        else:
            self.stdout.write(self.style.WARNING(f'\n⚠️ No se encontraron movimientos de reversa para eliminar'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ ¡Proceso completado! La factura {numero_factura} ha sido reactivada.'))
