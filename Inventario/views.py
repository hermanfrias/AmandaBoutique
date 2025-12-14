from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ExistenciaInsumo, CompraInsumo, UsoInsumo, DetalleUsoInsumo
from .forms import ExistenciaInsumoForm, CompraInsumoForm, UsoInsumoForm, DetalleUsoInsumoFormSet


# ==================== VISTAS PARA EXISTENCIA INSUMO ====================

@login_required
def listar_insumos(request):
    insumos = ExistenciaInsumo.objects.all()
    context = {
        'insumos': insumos,
    }
    return render(request, 'Inventario/listar_insumos.html', context)


@login_required
def crear_insumo(request):
    if request.method == 'POST':
        form = ExistenciaInsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo creado exitosamente.')
            return redirect('listar_insumos')
    else:
        form = ExistenciaInsumoForm()
    
    context = {
        'form': form,
        'accion': 'Crear',
    }
    return render(request, 'Inventario/form_insumo.html', context)


@login_required
def editar_insumo(request, pk):
    insumo = get_object_or_404(ExistenciaInsumo, pk=pk)
    if request.method == 'POST':
        form = ExistenciaInsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo actualizado exitosamente.')
            return redirect('listar_insumos')
    else:
        form = ExistenciaInsumoForm(instance=insumo)
    
    context = {
        'form': form,
        'accion': 'Editar',
        'insumo': insumo,
    }
    return render(request, 'Inventario/form_insumo.html', context)


@login_required
def eliminar_insumo(request, pk):
    insumo = get_object_or_404(ExistenciaInsumo, pk=pk)
    if request.method == 'POST':
        insumo.delete()
        messages.success(request, 'Insumo eliminado exitosamente.')
        return redirect('listar_insumos')
    
    context = {
        'insumo': insumo,
    }
    return render(request, 'Inventario/eliminar_insumo.html', context)


@login_required
def detalle_insumo(request, pk):
    insumo = get_object_or_404(ExistenciaInsumo, pk=pk)
    compras = insumo.compras.all()
    
    context = {
        'insumo': insumo,
        'compras': compras,
    }
    return render(request, 'Inventario/detalle_insumo.html', context)


# ==================== VISTAS PARA COMPRA INSUMO ====================

@login_required
def listar_compras(request):
    compras = CompraInsumo.objects.all()
    context = {
        'compras': compras,
    }
    return render(request, 'Inventario/listar_compras.html', context)


@login_required
def crear_compra(request):
    if request.method == 'POST':
        form = CompraInsumoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Compra registrada exitosamente.')
                return redirect('listar_compras')
            except Exception as e:
                messages.error(request, f'Error al guardar la compra: {str(e)}')
    else:
        form = CompraInsumoForm()
    
    context = {
        'form': form,
        'accion': 'Registrar',
    }
    return render(request, 'Inventario/form_compra.html', context)


@login_required
def editar_compra(request, pk):
    compra = get_object_or_404(CompraInsumo, pk=pk)
    if request.method == 'POST':
        form = CompraInsumoForm(request.POST, instance=compra)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Compra actualizada exitosamente.')
                return redirect('listar_compras')
            except Exception as e:
                messages.error(request, f'Error al actualizar la compra: {str(e)}')
    else:
        form = CompraInsumoForm(instance=compra)
    
    context = {
        'form': form,
        'accion': 'Editar',
        'compra': compra,
    }
    return render(request, 'Inventario/form_compra.html', context)


@login_required
def eliminar_compra(request, pk):
    compra = get_object_or_404(CompraInsumo, pk=pk)
    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra eliminada exitosamente.')
        return redirect('listar_compras')
    
    context = {
        'compra': compra,
    }
    return render(request, 'Inventario/eliminar_compra.html', context)


@login_required
def detalle_compra(request, pk):
    compra = get_object_or_404(CompraInsumo, pk=pk)
    
    context = {
        'compra': compra,
    }
    return render(request, 'Inventario/detalle_compra.html', context)


# ==================== VISTAS PARA USO DE INSUMOS ====================

@login_required
def listar_usos(request):
    usos = UsoInsumo.objects.all()
    context = {
        'usos': usos,
    }
    return render(request, 'Inventario/listar_usos.html', context)


@login_required
def crear_uso(request):
    if request.method == 'POST':
        form = UsoInsumoForm(request.POST)
        formset = DetalleUsoInsumoFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                # Guardar el uso
                uso = form.save()
                
                # Guardar los detalles
                formset.instance = uso
                detalles = formset.save()
                
                # Recargar el uso para obtener el costo actualizado
                uso.refresh_from_db()
                
                messages.success(request, f'Uso registrado exitosamente. Costo total: ${uso.costo_total_usd:.2f} USD')
                return redirect('listar_usos')
            except ValidationError as e:
                messages.error(request, f'Error de validación: {e}')
            except Exception as e:
                messages.error(request, f'Error al registrar el uso: {str(e)}')
        else:
            if form.errors:
                messages.error(request, f'Errores en el formulario: {form.errors}')
            if formset.errors:
                messages.error(request, f'Errores en los detalles: {formset.errors}')
    else:
        form = UsoInsumoForm()
        formset = DetalleUsoInsumoFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'accion': 'Registrar',
    }
    return render(request, 'Inventario/form_uso.html', context)



@login_required
def editar_uso(request, pk):
    uso = get_object_or_404(UsoInsumo, pk=pk)
    
    if request.method == 'POST':
        form = UsoInsumoForm(request.POST, instance=uso)
        formset = DetalleUsoInsumoFormSet(request.POST, instance=uso)
        
        if form.is_valid() and formset.is_valid():
            try:
                # Guardar el uso
                form.save()
                
                # Guardar los detalles (esto manejará las adiciones, modificaciones y eliminaciones)
                formset.save()
                
                # Recalcular el costo total
                uso.calcular_costo_total()
                
                messages.success(request, f'Uso actualizado exitosamente. Costo total: ${uso.costo_total_usd:.2f} USD')
                return redirect('listar_usos')
            except Exception as e:
                messages.error(request, f'Error al actualizar el uso: {str(e)}')
    else:
        form = UsoInsumoForm(instance=uso)
        formset = DetalleUsoInsumoFormSet(instance=uso)
    
    context = {
        'form': form,
        'formset': formset,
        'accion': 'Editar',
        'uso': uso,
    }
    return render(request, 'Inventario/form_uso.html', context)


@login_required
def detalle_uso(request, pk):
    uso = get_object_or_404(UsoInsumo, pk=pk)
    detalles = uso.detalles.all()
    
    context = {
        'uso': uso,
        'detalles': detalles,
    }
    return render(request, 'Inventario/detalle_uso.html', context)


@login_required
def eliminar_uso(request, pk):
    uso = get_object_or_404(UsoInsumo, pk=pk)
    if request.method == 'POST':
        # Los detalles se eliminarán en cascada y restaurarán las existencias
        uso.delete()
        messages.success(request, 'Uso eliminado exitosamente. Las existencias han sido restauradas.')
        return redirect('listar_usos')
    
    context = {
        'uso': uso,
    }
    return render(request, 'Inventario/eliminar_uso.html', context)

