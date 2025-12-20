"""
Vistas para el módulo de Activos Fijos
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import datetime

from .models import ActivoFijo
from .forms import ActivoFijoForm, MantenimientoForm


def listar_activos(request):
    """Lista todos los activos fijos con filtros"""
    activos = ActivoFijo.objects.all()
    
    # Filtros
    tipo_filtro = request.GET.get('tipo', '')
    estado_filtro = request.GET.get('estado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    buscar = request.GET.get('buscar', '')
    
    if tipo_filtro:
        activos = activos.filter(tipo_activo=tipo_filtro)
    
    if estado_filtro:
        activos = activos.filter(estado=estado_filtro)
    
    if fecha_desde:
        activos = activos.filter(fecha_adquisicion__gte=fecha_desde)
    
    if fecha_hasta:
        activos = activos.filter(fecha_adquisicion__lte=fecha_hasta)
    
    if buscar:
        activos = activos.filter(
            Q(numero_inventario__icontains=buscar) |
            Q(marca__icontains=buscar) |
            Q(modelo__icontains=buscar) |
            Q(serial__icontains=buscar)
        )
    
    # Calcular totales
    total_activos = activos.count()
    valor_total = activos.aggregate(total=Sum('valor_dolares'))['total'] or 0
    depreciacion_total = activos.aggregate(total=Sum('depreciacion_acumulada'))['total'] or 0
    valor_actual_total = activos.aggregate(total=Sum('valor_actual'))['total'] or 0
    
    context = {
        'activos': activos,
        'tipo_filtro': tipo_filtro,
        'estado_filtro': estado_filtro,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'buscar': buscar,
        'total_activos': total_activos,
        'valor_total': valor_total,
        'depreciacion_total': depreciacion_total,
        'valor_actual_total': valor_actual_total,
        'tipos_activo': ActivoFijo.TIPO_ACTIVO_CHOICES,
        'estados': ActivoFijo.ESTADO_CHOICES,
    }
    
    return render(request, 'Inventario/listar_activos.html', context)


def crear_activo(request):
    """Crea un nuevo activo fijo"""
    if request.method == 'POST':
        form = ActivoFijoForm(request.POST, request.FILES)
        if form.is_valid():
            activo = form.save()
            messages.success(request, f'Activo {activo.numero_inventario} creado exitosamente.')
            return redirect('detalle_activo', numero_inventario=activo.numero_inventario)
    else:
        form = ActivoFijoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Activo Fijo',
        'accion': 'Crear',
    }
    
    return render(request, 'Inventario/form_activo.html', context)


def editar_activo(request, numero_inventario):
    """Edita un activo fijo existente"""
    activo = get_object_or_404(ActivoFijo, numero_inventario=numero_inventario)
    
    if request.method == 'POST':
        form = ActivoFijoForm(request.POST, request.FILES, instance=activo)
        if form.is_valid():
            activo = form.save()
            messages.success(request, f'Activo {activo.numero_inventario} actualizado exitosamente.')
            return redirect('detalle_activo', numero_inventario=activo.numero_inventario)
    else:
        form = ActivoFijoForm(instance=activo)
    
    context = {
        'form': form,
        'activo': activo,
        'titulo': f'Editar Activo {activo.numero_inventario}',
        'accion': 'Actualizar',
    }
    
    return render(request, 'Inventario/form_activo.html', context)


def detalle_activo(request, numero_inventario):
    """Muestra el detalle completo de un activo fijo"""
    activo = get_object_or_404(ActivoFijo, numero_inventario=numero_inventario)
    
    # Recalcular depreciación para mostrar valores actualizados
    activo.calcular_depreciacion()
    
    context = {
        'activo': activo,
        'vida_util_restante': activo.get_vida_util_restante(),
        'porcentaje_depreciacion': activo.get_porcentaje_depreciacion(),
    }
    
    return render(request, 'Inventario/detalle_activo.html', context)


def eliminar_activo(request, numero_inventario):
    """Elimina un activo fijo"""
    activo = get_object_or_404(ActivoFijo, numero_inventario=numero_inventario)
    
    if request.method == 'POST':
        numero = activo.numero_inventario
        activo.delete()
        messages.success(request, f'Activo {numero} eliminado exitosamente.')
        return redirect('listar_activos')
    
    context = {
        'activo': activo,
    }
    
    return render(request, 'Inventario/eliminar_activo.html', context)


def registrar_mantenimiento(request, numero_inventario):
    """Registra mantenimiento para un activo fijo"""
    activo = get_object_or_404(ActivoFijo, numero_inventario=numero_inventario)
    
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Mantenimiento registrado para activo {activo.numero_inventario}.')
            return redirect('detalle_activo', numero_inventario=activo.numero_inventario)
    else:
        form = MantenimientoForm(instance=activo)
    
    context = {
        'form': form,
        'activo': activo,
    }
    
    return render(request, 'Inventario/form_mantenimiento.html', context)


def activos_pdf(request):
    """Genera PDF con el listado de activos fijos"""
    activos = ActivoFijo.objects.all()
    
    # Aplicar los mismos filtros que en la vista de listado
    tipo_filtro = request.GET.get('tipo', '')
    estado_filtro = request.GET.get('estado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    buscar = request.GET.get('buscar', '')
    
    if tipo_filtro:
        activos = activos.filter(tipo_activo=tipo_filtro)
    
    if estado_filtro:
        activos = activos.filter(estado=estado_filtro)
    
    if fecha_desde:
        activos = activos.filter(fecha_adquisicion__gte=fecha_desde)
    
    if fecha_hasta:
        activos = activos.filter(fecha_adquisicion__lte=fecha_hasta)
    
    if buscar:
        activos = activos.filter(
            Q(numero_inventario__icontains=buscar) |
            Q(marca__icontains=buscar) |
            Q(modelo__icontains=buscar) |
            Q(serial__icontains=buscar)
        )
    
    # Calcular totales
    total_activos = activos.count()
    valor_total = activos.aggregate(total=Sum('valor_dolares'))['total'] or 0
    depreciacion_total = activos.aggregate(total=Sum('depreciacion_acumulada'))['total'] or 0
    valor_actual_total = activos.aggregate(total=Sum('valor_actual'))['total'] or 0
    
    # Totales por tipo
    totales_por_tipo = {}
    for tipo, _ in ActivoFijo.TIPO_ACTIVO_CHOICES:
        activos_tipo = activos.filter(tipo_activo=tipo)
        if activos_tipo.exists():
            totales_por_tipo[tipo] = {
                'cantidad': activos_tipo.count(),
                'valor_total': activos_tipo.aggregate(total=Sum('valor_dolares'))['total'] or 0,
                'valor_actual': activos_tipo.aggregate(total=Sum('valor_actual'))['total'] or 0,
            }
    
    context = {
        'activos': activos,
        'fecha_generacion': datetime.now(),
        'total_activos': total_activos,
        'valor_total': valor_total,
        'depreciacion_total': depreciacion_total,
        'valor_actual_total': valor_actual_total,
        'totales_por_tipo': totales_por_tipo,
        'tipo_filtro': tipo_filtro,
        'estado_filtro': estado_filtro,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'buscar': buscar,
    }
    
    html_string = render_to_string('Inventario/activos_pdf.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="activos_fijos_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response
