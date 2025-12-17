from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import CompraInsumo
from .forms import CompraInsumoForm

# ==================== VISTAS PARA COMPRAS AGRUPADAS POR FACTURA ====================

@login_required
def detalle_compra_grupo(request, numero_factura, fecha):
    """Vista para ver el detalle de todas las compras de una factura"""
    from datetime import datetime
    
    # Convertir fecha de string a date
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    # Obtener todas las compras con ese número de factura y fecha
    compras = CompraInsumo.objects.filter(
        numero_factura=numero_factura,
        fecha_compra=fecha_obj
    ).order_by('insumo__codigo')
    
    if not compras.exists():
        messages.error(request, 'No se encontraron compras con ese número de factura y fecha.')
        return redirect('listar_compras')
    
    # Calcular totales
    total_bs = sum(c.monto_total_bs or 0 for c in compras)
    total_usd = sum(c.monto_total_usd or 0 for c in compras)
    subtotal_bs = sum(c.monto_bs or 0 for c in compras)
    subtotal_usd = sum(c.monto_usd or 0 for c in compras)
    iva_bs = sum(c.monto_iva_bs or 0 for c in compras)
    iva_usd = sum(c.monto_iva_usd or 0 for c in compras)
    
    context = {
        'numero_factura': numero_factura,
        'fecha_compra': fecha_obj,
        'moneda': compras.first().moneda,
        'aplicar_iva': compras.first().aplicar_iva,
        'compras': compras,
        'subtotal_bs': subtotal_bs,
        'subtotal_usd': subtotal_usd,
        'iva_bs': iva_bs,
        'iva_usd': iva_usd,
        'total_bs': total_bs,
        'total_usd': total_usd,
    }
    return render(request, 'Inventario/detalle_compra_grupo.html', context)


@login_required
def editar_compra_grupo(request, numero_factura, fecha):
    """Vista para editar todas las compras de una factura (permitir eliminar ítems)"""
    from datetime import datetime
    from django.forms import modelformset_factory
    
    # Convertir fecha de string a date
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    # Obtener todas las compras con ese número de factura y fecha
    compras = CompraInsumo.objects.filter(
        numero_factura=numero_factura,
        fecha_compra=fecha_obj
    )
    
    if not compras.exists():
        messages.error(request, 'No se encontraron compras con ese número de factura y fecha.')
        return redirect('listar_compras')
    
    # Crear formset para editar múltiples compras
    # Solo permitir editar insumo, cantidad y monto
    # Los campos fecha_compra, numero_factura, moneda y aplicar_iva son comunes y no se editan
    CompraFormSet = modelformset_factory(
        CompraInsumo,
        fields=['insumo', 'cantidad', 'monto'],
        extra=0,
        can_delete=True,
        widgets={
            'insumo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    )
    
    if request.method == 'POST':
        formset = CompraFormSet(request.POST, queryset=compras)
        if formset.is_valid():
            try:
                formset.save()
                messages.success(request, 'Compras actualizadas exitosamente.')
                return redirect('listar_compras')
            except Exception as e:
                messages.error(request, f'Error al actualizar las compras: {str(e)}')
        else:
            messages.error(request, f'Errores en el formulario. Por favor revise los campos.')
    else:
        formset = CompraFormSet(queryset=compras)
    
    context = {
        'formset': formset,
        'numero_factura': numero_factura,
        'fecha_compra': fecha_obj,
        'accion': 'Editar',
    }
    return render(request, 'Inventario/editar_compra_grupo.html', context)


@login_required
def anular_compra_grupo(request, numero_factura, fecha):
    """Anula todas las compras de una factura (reemplaza eliminar_compra_grupo)"""
    from datetime import datetime
    
    # Convertir fecha de string a date
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    # Obtener todas las compras con ese número de factura y fecha
    compras = CompraInsumo.objects.filter(
        numero_factura=numero_factura,
        fecha_compra=fecha_obj
    )
    
    if not compras.exists():
        messages.error(request, 'No se encontraron compras con ese número de factura y fecha.')
        return redirect('listar_compras')
    
    # Verificar si ya están anuladas
    if compras.filter(anulada=True).exists():
        messages.warning(request, 'Algunas o todas las compras de esta factura ya están anuladas.')
        return redirect('listar_compras')
    
    if request.method == 'POST':
        try:
            cantidad = compras.count()
            print(f"\n{'='*80}")
            print(f"🟢 VISTA: Iniciando anulación de {cantidad} compra(s) de factura {numero_factura}")
            print(f"{'='*80}\n")
            
            # Anular cada compra (esto revertirá inventario y creará movimientos de reversa)
            for i, compra in enumerate(compras, 1):
                print(f"\n--- Anulando compra {i}/{cantidad} ---")
                compra.anular()
                print(f"--- Compra {i} anulada ---\n")
            
            print(f"\n{'='*80}")
            print(f"🟢 VISTA: Anulación completada exitosamente")
            print(f"{'='*80}\n")
            
            messages.success(request, f'Se anularon {cantidad} compra(s) exitosamente. Se han creado movimientos de reversa en el flujo de caja.')
            return redirect('listar_compras')
        except Exception as e:
            print(f"\n❌ ERROR EN VISTA: {type(e).__name__}: {str(e)}")
            import traceback
            print(traceback.format_exc())
            messages.error(request, f'Error al anular las compras: {str(e)}')
    
    # Calcular total para mostrar
    total_usd = sum(c.monto_total_usd or 0 for c in compras)
    
    context = {
        'numero_factura': numero_factura,
        'fecha_compra': fecha_obj,
        'compras': compras,
        'total_usd': total_usd,
    }
    return render(request, 'Inventario/anular_compra_grupo.html', context)

