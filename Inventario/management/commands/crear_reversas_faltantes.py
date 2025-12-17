from django.core.management.base import BaseCommand
from Inventario.models import CompraInsumo
from flujo.models import MovimientoCaja


class Command(BaseCommand):
    help = 'Crea movimientos de reversa para compras ya anuladas'

    def handle(self, *args, **options):
        # Buscar compras anuladas sin movimiento de reversa
        compras_anuladas = CompraInsumo.objects.filter(anulada=True)
        
        self.stdout.write(f"\nEncontradas {compras_anuladas.count()} compras anuladas")
        
        creados = 0
        ya_existian = 0
        
        for compra in compras_anuladas:
            # Verificar si ya existe movimiento de reversa
            descripcion_reversa = f"REVERSA - Anulación Factura {compra.numero_factura}" if compra.numero_factura else "REVERSA - Anulación compra insumos"
            
            existe = MovimientoCaja.objects.filter(
                numero_factura=compra.numero_factura,
                descripcion=descripcion_reversa
            ).exists()
            
            if existe:
                ya_existian += 1
                continue
            
            # Crear movimiento de reversa
            if compra.moneda == 'Bs':
                monto_reversa = compra.monto_total_bs
            else:
                monto_reversa = compra.monto_total_usd
            
            MovimientoCaja.objects.create(
                fecha=compra.fecha_compra,
                descripcion=descripcion_reversa,
                tipo='Ingreso',
                tipo_movimiento='Compra de Insumos',
                metodo_pago='Efectivo',
                moneda=compra.moneda,
                monto=monto_reversa,
                numero_factura=compra.numero_factura
            )
            
            self.stdout.write(self.style.SUCCESS(f"✅ Creada reversa para factura {compra.numero_factura}: {monto_reversa} {compra.moneda}"))
            creados += 1
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(self.style.SUCCESS(f"Movimientos de reversa creados: {creados}"))
        self.stdout.write(f"Ya existían: {ya_existian}")
        self.stdout.write(f"{'='*60}\n")
