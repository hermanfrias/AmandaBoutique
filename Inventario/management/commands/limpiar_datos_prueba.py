from django.core.management.base import BaseCommand
from Inventario.models import CompraInsumo
from flujo.models import MovimientoCaja


class Command(BaseCommand):
    help = 'Elimina todas las compras anuladas y sus movimientos asociados (de prueba)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirmar la eliminación',
        )

    def handle(self, *args, **options):
        if not options['confirmar']:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  ADVERTENCIA: Este comando eliminará PERMANENTEMENTE:\n'
                '   - Todas las compras anuladas\n'
                '   - Todos los movimientos de reversa\n'
                '   - Todos los movimientos de compra asociados\n\n'
                'Para confirmar, ejecuta:\n'
                '  python manage.py limpiar_datos_prueba --confirmar\n'
            ))
            return
        
        self.stdout.write('\n' + '='*80)
        self.stdout.write('LIMPIEZA DE DATOS DE PRUEBA')
        self.stdout.write('='*80 + '\n')
        
        # 1. Obtener todas las compras anuladas
        compras_anuladas = CompraInsumo.objects.filter(anulada=True)
        total_compras = compras_anuladas.count()
        
        self.stdout.write(f'\n📋 Compras anuladas encontradas: {total_compras}')
        
        if total_compras == 0:
            self.stdout.write(self.style.SUCCESS('\n✅ No hay compras anuladas para eliminar'))
            return
        
        # Obtener números de factura únicos
        facturas_anuladas = set()
        for compra in compras_anuladas:
            if compra.numero_factura:
                facturas_anuladas.add(compra.numero_factura)
        
        self.stdout.write(f'\nFacturas afectadas: {", ".join(sorted(facturas_anuladas))}')
        
        # 2. Eliminar movimientos de reversa
        movimientos_reversa = MovimientoCaja.objects.filter(descripcion__icontains='REVERSA')
        total_reversas = movimientos_reversa.count()
        
        self.stdout.write(f'\n💰 Movimientos de REVERSA encontrados: {total_reversas}')
        
        if total_reversas > 0:
            movimientos_reversa.delete()
            self.stdout.write(self.style.SUCCESS(f'   ✅ {total_reversas} movimientos de reversa eliminados'))
        
        # 3. Eliminar movimientos de compra asociados a facturas anuladas
        movimientos_compra = MovimientoCaja.objects.filter(
            numero_factura__in=facturas_anuladas,
            tipo_movimiento='Compra de Insumos'
        ).exclude(descripcion__icontains='REVERSA')
        
        total_mov_compra = movimientos_compra.count()
        
        self.stdout.write(f'\n💰 Movimientos de compra asociados: {total_mov_compra}')
        
        if total_mov_compra > 0:
            movimientos_compra.delete()
            self.stdout.write(self.style.SUCCESS(f'   ✅ {total_mov_compra} movimientos de compra eliminados'))
        
        # 4. Eliminar las compras anuladas
        self.stdout.write(f'\n📦 Eliminando {total_compras} compras anuladas...')
        compras_anuladas.delete()
        self.stdout.write(self.style.SUCCESS(f'   ✅ {total_compras} compras anuladas eliminadas'))
        
        # Resumen
        self.stdout.write('\n' + '='*80)
        self.stdout.write('RESUMEN DE ELIMINACIÓN')
        self.stdout.write('='*80)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Compras anuladas eliminadas: {total_compras}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Movimientos de reversa eliminados: {total_reversas}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Movimientos de compra eliminados: {total_mov_compra}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Total de registros eliminados: {total_compras + total_reversas + total_mov_compra}'))
        self.stdout.write('\n' + '='*80 + '\n')
