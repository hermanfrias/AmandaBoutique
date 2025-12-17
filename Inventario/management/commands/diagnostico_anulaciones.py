from django.core.management.base import BaseCommand
from Inventario.models import CompraInsumo
from flujo.models import MovimientoCaja


class Command(BaseCommand):
    help = 'Verifica el estado de anulaciones y movimientos de caja'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write("DIAGNÓSTICO: Anulaciones y Movimientos de Caja")
        self.stdout.write("="*80 + "\n")
        
        # 1. Verificar compras anuladas
        compras_anuladas = CompraInsumo.objects.filter(anulada=True)
        self.stdout.write(f"\n📋 Total de compras anuladas: {compras_anuladas.count()}")
        
        if compras_anuladas.exists():
            self.stdout.write("\nDetalles de compras anuladas:")
            for compra in compras_anuladas:
                self.stdout.write(f"\n  - ID: {compra.pk}")
                self.stdout.write(f"    Factura: {compra.numero_factura}")
                self.stdout.write(f"    Fecha compra: {compra.fecha_compra}")
                self.stdout.write(f"    Fecha anulación: {compra.fecha_anulacion}")
                self.stdout.write(f"    Monto: {compra.monto_total_usd} USD")
        
        # 2. Verificar movimientos de reversa
        movimientos_reversa = MovimientoCaja.objects.filter(descripcion__icontains="REVERSA")
        self.stdout.write(f"\n\n💰 Total de movimientos de REVERSA: {movimientos_reversa.count()}")
        
        if movimientos_reversa.exists():
            self.stdout.write("\nDetalles de movimientos de reversa:")
            for mov in movimientos_reversa:
                self.stdout.write(f"\n  - ID: {mov.pk}")
                self.stdout.write(f"    Descripción: {mov.descripcion}")
                self.stdout.write(f"    Fecha: {mov.fecha}")
                self.stdout.write(f"    Tipo: {mov.tipo}")
                self.stdout.write(f"    Monto: {mov.monto} {mov.moneda}")
                self.stdout.write(f"    Número factura: {mov.numero_factura}")
        
        # 3. Verificar movimientos por factura
        self.stdout.write("\n\n🔍 Verificando movimientos por factura anulada:")
        for compra in compras_anuladas:
            if compra.numero_factura:
                movs = MovimientoCaja.objects.filter(numero_factura=compra.numero_factura)
                self.stdout.write(f"\n  Factura {compra.numero_factura}:")
                self.stdout.write(f"    Total movimientos: {movs.count()}")
                for mov in movs:
                    self.stdout.write(f"      - {mov.tipo}: {mov.monto} {mov.moneda} - {mov.descripcion}")
        
        # 4. Resumen
        self.stdout.write("\n\n" + "="*80)
        self.stdout.write("RESUMEN")
        self.stdout.write("="*80)
        self.stdout.write(f"\n✅ Compras anuladas: {compras_anuladas.count()}")
        self.stdout.write(f"✅ Movimientos de reversa: {movimientos_reversa.count()}")
        
        if compras_anuladas.count() > 0 and movimientos_reversa.count() == 0:
            self.stdout.write(self.style.ERROR("\n⚠️ PROBLEMA DETECTADO: Hay compras anuladas pero NO hay movimientos de reversa"))
            self.stdout.write(self.style.WARNING("   Esto indica que el signal NO está creando los movimientos de reversa"))
        elif compras_anuladas.count() == movimientos_reversa.count():
            self.stdout.write(self.style.SUCCESS("\n✅ TODO CORRECTO: Cada compra anulada tiene su movimiento de reversa"))
        
        self.stdout.write("\n" + "="*80 + "\n")
