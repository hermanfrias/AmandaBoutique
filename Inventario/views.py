from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import ExistenciaInsumo, CompraInsumo, UsoInsumo, DetalleUsoInsumo
from .forms import ExistenciaInsumoForm, CompraInsumoForm, UsoInsumoForm, DetalleUsoInsumoFormSet


# ==================== VISTAS PARA EXISTENCIA INSUMO ====================

@login_required
def listar_insumos(request):
    insumos = ExistenciaInsumo.objects.all()
    
    # Ordenamiento
    order_by = request.GET.get('order_by', 'codigo')  # Por defecto ordenar por código
    if order_by in ['codigo', 'descripcion', '-codigo', '-descripcion']:
        insumos = insumos.order_by(order_by)
    else:
        insumos = insumos.order_by('codigo')
    
    # Búsqueda dinámica por descripción
    search_query = request.GET.get('search', '')
    if search_query:
        insumos = insumos.filter(descripcion__icontains=search_query)
    
    # Filtros por categoría y proveedor
    categoria_filtro = request.GET.get('categoria', '')
    proveedor_filtro = request.GET.get('proveedor', '')
    
    if categoria_filtro:
        insumos = insumos.filter(categoria=categoria_filtro)
    
    if proveedor_filtro:
        insumos = insumos.filter(proveedor_id=proveedor_filtro)
    
    # Obtener listas para los filtros
    from ProveedoresApp.models import Proveedores
    categorias = ExistenciaInsumo.CATEGORIA_CHOICES
    proveedores = Proveedores.objects.all().order_by('nombre')
    
    context = {
        'insumos': insumos,
        'search_query': search_query,
        'order_by': order_by,
        'categorias': categorias,
        'proveedores': proveedores,
        'categoria_filtro': categoria_filtro,
        'proveedor_filtro': proveedor_filtro,
    }
    return render(request, 'Inventario/listar_insumos.html', context)


@login_required
def crear_insumo(request):
    if request.method == 'POST':
        form = ExistenciaInsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_insumo')
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
    
    # Filtros por fecha
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    
    if fecha_desde:
        compras = compras.filter(fecha_compra__gte=fecha_desde)
    
    if fecha_hasta:
        compras = compras.filter(fecha_compra__lte=fecha_hasta)
    
    context = {
        'compras': compras,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }
    return render(request, 'Inventario/listar_compras.html', context)


@login_required
def crear_compra(request):
    if request.method == 'POST':
        form = CompraInsumoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
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


@login_required
def compras_pdf(request):
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from weasyprint import HTML, CSS
    from django.conf import settings
    from decimal import Decimal
    import os
    import traceback
    import datetime

    try:
        compras = CompraInsumo.objects.all()
        
        # Aplicar filtros de fecha
        fecha_desde = request.GET.get('fecha_desde', '')
        fecha_hasta = request.GET.get('fecha_hasta', '')
        
        if fecha_desde:
            compras = compras.filter(fecha_compra__gte=fecha_desde)
        
        if fecha_hasta:
            compras = compras.filter(fecha_compra__lte=fecha_hasta)
        
        # Calcular totales
        total_compras = compras.count()
        total_bs = sum(compra.monto_total_bs for compra in compras)
        total_usd = sum(compra.monto_total_usd for compra in compras)
        
        html_string = render_to_string('Inventario/compras_pdf.html', {
            'compras': compras,
            'total_compras': total_compras,
            'total_bs': total_bs,
            'total_usd': total_usd,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'fecha_generacion': datetime.date.today(),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="listado_compras.pdf"'

        css_path = os.path.join(settings.STATICFILES_DIRS[0], "BoutiqueApp/css/pdf.css")

        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            response, stylesheets=[CSS(css_path)]
        )
        return response
    except Exception as e:
        error_msg = f"Error generando PDF: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print("=" * 80)
        print(error_msg)
        print("=" * 80)
        return HttpResponse(f"<pre>{error_msg}</pre>", status=500)


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


# ==================== VISTA PARA PDF DE INSUMOS ====================

@login_required
def insumos_pdf(request):
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from weasyprint import HTML, CSS
    from django.conf import settings
    from decimal import Decimal
    import os
    import traceback
    import datetime

    try:
        insumos = ExistenciaInsumo.objects.all()
        
        # Respetar el ordenamiento del listado
        order_by = request.GET.get('order_by', 'codigo')
        if order_by in ['codigo', 'descripcion', '-codigo', '-descripcion']:
            insumos = insumos.order_by(order_by)
        else:
            insumos = insumos.order_by('codigo')
        
        # Aplicar filtros de categoría y proveedor
        categoria_filtro = request.GET.get('categoria', '')
        proveedor_filtro = request.GET.get('proveedor', '')
        
        if categoria_filtro:
            insumos = insumos.filter(categoria=categoria_filtro)
        
        if proveedor_filtro:
            insumos = insumos.filter(proveedor_id=proveedor_filtro)
        
        # Calcular totales
        total_insumos = insumos.count()
        
        # Calcular valor total del inventario (existencia * costo_dolar)
        valor_total_inventario = Decimal('0')
        for insumo in insumos:
            if insumo.costo_dolar and insumo.existencia:
                valor_total_inventario += insumo.existencia * insumo.costo_dolar
        
        # Contar insumos bajo existencia mínima
        insumos_bajo_minimo = insumos.filter(existencia__lt=models.F('existencia_minima')).count()
        
        html_string = render_to_string('Inventario/insumos_pdf.html', {
            'insumos': insumos,
            'total_insumos': total_insumos,
            'valor_total_inventario': valor_total_inventario,
            'insumos_bajo_minimo': insumos_bajo_minimo,
            'fecha_generacion': datetime.date.today(),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="listado_insumos.pdf"'

        css_path = os.path.join(settings.STATICFILES_DIRS[0], "BoutiqueApp/css/pdf.css")

        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            response, stylesheets=[CSS(css_path)]
        )
        return response
    except Exception as e:
        # Mostrar el error completo para debugging
        error_msg = f"Error generando PDF: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print("=" * 80)
        print(error_msg)
        print("=" * 80)
        return HttpResponse(f"<pre>{error_msg}</pre>", status=500)
