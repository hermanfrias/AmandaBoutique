from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Vestido, Alquiler
from .forms import VestidoForm, AlquilerForm, ClienteRapidoForm
from ClientesApp.models import Clientes
from datetime import date


# ============================================
# VISTAS PARA VESTIDOS
# ============================================

@login_required
def listar_vestidos(request):
    """Lista todos los vestidos con filtros por estado"""
    vestidos = Vestido.objects.all()
    
    # Filtro por estado
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        vestidos = vestidos.filter(estado=estado_filtro)
    
    # Búsqueda por nombre o color
    buscar = request.GET.get('buscar', '')
    if buscar:
        vestidos = vestidos.filter(
            Q(nombre_modelo__icontains=buscar) |
            Q(color__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )
    
    context = {
        'vestidos': vestidos,
        'estado_filtro': estado_filtro,
        'buscar': buscar,
        'estados': Vestido.ESTADO_CHOICES,
    }
    return render(request, 'alquiler/listar_vestidos.html', context)


@login_required
def crear_vestido(request):
    """Crea un nuevo vestido"""
    if request.method == 'POST':
        form = VestidoForm(request.POST, request.FILES)
        if form.is_valid():
            vestido = form.save()
            messages.success(request, f'Vestido "{vestido.nombre_modelo}" creado exitosamente.')
            return redirect('listar_vestidos')
    else:
        form = VestidoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Vestido',
        'accion': 'Crear'
    }
    return render(request, 'alquiler/form_vestido.html', context)


@login_required
def editar_vestido(request, pk):
    """Edita un vestido existente"""
    vestido = get_object_or_404(Vestido, pk=pk)
    
    if request.method == 'POST':
        form = VestidoForm(request.POST, request.FILES, instance=vestido)
        if form.is_valid():
            vestido = form.save()
            messages.success(request, f'Vestido "{vestido.nombre_modelo}" actualizado exitosamente.')
            return redirect('detalle_vestido', pk=vestido.pk)
    else:
        form = VestidoForm(instance=vestido)
    
    context = {
        'form': form,
        'vestido': vestido,
        'titulo': 'Editar Vestido',
        'accion': 'Actualizar'
    }
    return render(request, 'alquiler/form_vestido.html', context)


@login_required
def detalle_vestido(request, pk):
    """Muestra los detalles de un vestido"""
    vestido = get_object_or_404(Vestido, pk=pk)
    alquileres = vestido.alquileres.all()[:5]  # Últimos 5 alquileres
    
    context = {
        'vestido': vestido,
        'alquileres': alquileres,
    }
    return render(request, 'alquiler/detalle_vestido.html', context)


@login_required
def eliminar_vestido(request, pk):
    """Elimina un vestido"""
    vestido = get_object_or_404(Vestido, pk=pk)
    
    if request.method == 'POST':
        nombre = vestido.nombre_modelo
        vestido.delete()
        messages.success(request, f'Vestido "{nombre}" eliminado exitosamente.')
        return redirect('listar_vestidos')
    
    context = {
        'vestido': vestido,
    }
    return render(request, 'alquiler/eliminar_vestido.html', context)


# ============================================
# VISTAS PARA ALQUILERES
# ============================================

@login_required
def listar_alquileres(request):
    """Lista todos los alquileres con filtros"""
    alquileres = Alquiler.objects.select_related('cliente', 'vestido').all()
    
    # Filtro por estado de pago
    estado_pago_filtro = request.GET.get('estado_pago', '')
    if estado_pago_filtro:
        alquileres = alquileres.filter(estado_pago=estado_pago_filtro)
    
    # Filtro por estado de alquiler
    estado_alquiler_filtro = request.GET.get('estado_alquiler', '')
    if estado_alquiler_filtro:
        alquileres = alquileres.filter(estado_alquiler=estado_alquiler_filtro)
    
    # Búsqueda por cliente
    buscar = request.GET.get('buscar', '')
    if buscar:
        alquileres = alquileres.filter(
            Q(cliente__nombre__icontains=buscar) |
            Q(cliente__apellido__icontains=buscar) |
            Q(vestido__nombre_modelo__icontains=buscar)
        )
    
    context = {
        'alquileres': alquileres,
        'estado_pago_filtro': estado_pago_filtro,
        'estado_alquiler_filtro': estado_alquiler_filtro,
        'buscar': buscar,
        'estados_pago': Alquiler.ESTADO_PAGO_CHOICES,
        'estados_alquiler': Alquiler.ESTADO_ALQUILER_CHOICES,
    }
    return render(request, 'alquiler/listar_alquileres.html', context)


@login_required
def crear_alquiler(request):
    """Crea un nuevo alquiler"""
    if request.method == 'POST':
        form = AlquilerForm(request.POST)
        if form.is_valid():
            try:
                alquiler = form.save()
                messages.success(request, f'Alquiler creado exitosamente para {alquiler.cliente.nombre} {alquiler.cliente.apellido}.')
                return redirect('detalle_alquiler', pk=alquiler.pk)
            except Exception as e:
                messages.error(request, f'Error al crear el alquiler: {str(e)}')
    else:
        # Establecer fecha de contrato por defecto a hoy
        form = AlquilerForm(initial={'fecha_contrato': date.today()})
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Alquiler',
        'accion': 'Crear'
    }
    return render(request, 'alquiler/form_alquiler.html', context)


@login_required
def editar_alquiler(request, pk):
    """Edita un alquiler existente"""
    alquiler = get_object_or_404(Alquiler, pk=pk)
    
    if request.method == 'POST':
        form = AlquilerForm(request.POST, instance=alquiler)
        if form.is_valid():
            try:
                alquiler = form.save()
                messages.success(request, f'Alquiler #{alquiler.pk} actualizado exitosamente.')
                return redirect('detalle_alquiler', pk=alquiler.pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar el alquiler: {str(e)}')
    else:
        form = AlquilerForm(instance=alquiler)
    
    context = {
        'form': form,
        'alquiler': alquiler,
        'titulo': 'Editar Alquiler',
        'accion': 'Actualizar'
    }
    return render(request, 'alquiler/form_alquiler.html', context)


@login_required
def detalle_alquiler(request, pk):
    """Muestra los detalles de un alquiler"""
    alquiler = get_object_or_404(Alquiler.objects.select_related('cliente', 'vestido'), pk=pk)
    saldo_pendiente = alquiler.calcular_saldo_pendiente()
    
    context = {
        'alquiler': alquiler,
        'saldo_pendiente': saldo_pendiente,
    }
    return render(request, 'alquiler/detalle_alquiler.html', context)


@login_required
def eliminar_alquiler(request, pk):
    """Elimina un alquiler"""
    alquiler = get_object_or_404(Alquiler, pk=pk)
    
    if request.method == 'POST':
        # Si el alquiler está activo, liberar el vestido
        if alquiler.estado_alquiler == 'Activo' and alquiler.vestido.estado == 'Alquilado':
            alquiler.vestido.estado = 'Disponible'
            alquiler.vestido.save()
        
        alquiler_id = alquiler.pk
        alquiler.delete()
        messages.success(request, f'Alquiler #{alquiler_id} eliminado exitosamente.')
        return redirect('listar_alquileres')
    
    context = {
        'alquiler': alquiler,
    }
    return render(request, 'alquiler/eliminar_alquiler.html', context)


@login_required
def generar_contrato_pdf(request, pk):
    """Genera el PDF del contrato de alquiler"""
    from django.template.loader import get_template
    from xhtml2pdf import pisa
    from io import BytesIO
    
    alquiler = get_object_or_404(Alquiler.objects.select_related('cliente', 'vestido'), pk=pk)
    
    template = get_template('alquiler/contrato_pdf.html')
    context = {
        'alquiler': alquiler,
        'saldo_pendiente': alquiler.calcular_saldo_pendiente(),
        'fecha_generacion': date.today(),
    }
    
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="contrato_alquiler_{alquiler.pk}.pdf"'
        return response
    
    messages.error(request, 'Error al generar el PDF del contrato.')
    return redirect('detalle_alquiler', pk=pk)


# ============================================
# VISTA AJAX PARA CREAR CLIENTE RÁPIDO
# ============================================

@login_required
def crear_cliente_rapido(request):
    """Vista AJAX para crear un cliente rápido desde el formulario de alquiler"""
    if request.method == 'POST':
        form = ClienteRapidoForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({
                'success': True,
                'cliente_id': cliente.pk,
                'cliente_nombre': str(cliente)
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
