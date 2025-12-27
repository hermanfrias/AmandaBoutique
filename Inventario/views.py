from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import ExistenciaInsumo, CompraInsumo, UsoInsumo, DetalleUsoInsumo
from .forms import ExistenciaInsumoForm, CompraInsumoForm, CompraInsumoDetalleFormSet, UsoInsumoForm, DetalleUsoInsumoFormSet


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
    from django.db.models import Sum, Q
    from collections import defaultdict
    
    # Obtener filtros de fecha
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    # Filtrar compras
    compras = CompraInsumo.objects.all()
    
    if fecha_desde:
        compras = compras.filter(fecha_compra__gte=fecha_desde)
    if fecha_hasta:
        compras = compras.filter(fecha_compra__lte=fecha_hasta)
    
    # Agrupar por número de factura
    compras_agrupadas = []
    facturas_procesadas = set()
    
    for compra in compras.order_by('-fecha_compra', 'numero_factura'):
        # Crear una clave única para agrupar (numero_factura + fecha)
        clave = f"{compra.numero_factura or 'SIN_FACTURA'}_{compra.fecha_compra}"
        
        if clave not in facturas_procesadas:
            facturas_procesadas.add(clave)
            
            # Obtener todas las compras con el mismo numero_factura y fecha
            if compra.numero_factura:
                items = CompraInsumo.objects.filter(
                    numero_factura=compra.numero_factura,
                    fecha_compra=compra.fecha_compra
                )
            else:
                # Si no tiene número de factura, solo agrupar esta compra individual
                items = CompraInsumo.objects.filter(pk=compra.pk)
            
            # Calcular totales del grupo
            total_bs = sum(item.monto_total_bs or 0 for item in items)
            total_usd = sum(item.monto_total_usd or 0 for item in items)
            subtotal_bs = sum(item.monto_bs or 0 for item in items)
            subtotal_usd = sum(item.monto_usd or 0 for item in items)
            
            # Verificar si todas las compras están anuladas
            todas_anuladas = all(item.anulada for item in items)
            
            compras_agrupadas.append({
                'numero_factura': compra.numero_factura or '-',
                'fecha_compra': compra.fecha_compra,
                'moneda': compra.moneda,
                'aplicar_iva': compra.aplicar_iva,
                'cantidad_items': items.count(),
                'subtotal_bs': subtotal_bs,
                'subtotal_usd': subtotal_usd,
                'total_bs': total_bs,
                'total_usd': total_usd,
                'items': list(items),  # Lista de CompraInsumo para acceder a los IDs
                'primer_item_id': items.first().pk,  # Para el botón de ver/editar
                'anulada': todas_anuladas,  # Indicador de anulación
            })

    
    context = {
        'compras_agrupadas': compras_agrupadas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }
    return render(request, 'Inventario/listar_compras.html', context)


@login_required
def listar_compras_detallado(request):
    """Lista todas las compras sin agrupar por factura"""
    # Obtener filtros de fecha
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    insumo_filtro = request.GET.get('insumo', '')
    
    # Filtrar compras
    compras = CompraInsumo.objects.all().order_by('-fecha_compra', 'numero_factura')
    
    if fecha_desde:
        compras = compras.filter(fecha_compra__gte=fecha_desde)
    if fecha_hasta:
        compras = compras.filter(fecha_compra__lte=fecha_hasta)
    if insumo_filtro:
        compras = compras.filter(insumo__descripcion__icontains=insumo_filtro)
    
    context = {
        'compras': compras,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'insumo_filtro': insumo_filtro,
    }
    return render(request, 'Inventario/listar_compras_detallado.html', context)


@login_required
def crear_compra(request):
    if request.method == 'POST':
        # Datos del encabezado (campos que se repiten)
        numero_factura = request.POST.get('numero_factura')
        fecha_compra_str = request.POST.get('fecha_compra')
        moneda = request.POST.get('moneda')
        # NOTA: aplicar_iva ahora es por item, no global
        
        # Validar campos requeridos
        if not fecha_compra_str or not moneda:
            messages.error(request, 'Debe completar todos los campos del encabezado (Fecha de Compra y Moneda).')
            formset = CompraInsumoDetalleFormSet(request.POST)
            from ProveedoresApp.models import Proveedores
            proveedores = Proveedores.objects.all().order_by('nombre')
            context = {
                'formset': formset,
                'accion': 'Registrar',
                'numero_factura': numero_factura,
                'fecha_compra': fecha_compra_str,
                'moneda': moneda,
                'proveedores': proveedores,
            }
            return render(request, 'Inventario/form_compra.html', context)
        
        # Convertir fecha de string a date
        from datetime import datetime
        try:
            fecha_compra = datetime.strptime(fecha_compra_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Formato de fecha inválido.')
            formset = CompraInsumoDetalleFormSet(request.POST)
            from ProveedoresApp.models import Proveedores
            proveedores = Proveedores.objects.all().order_by('nombre')
            context = {
                'formset': formset,
                'accion': 'Registrar',
                'numero_factura': numero_factura,
                'fecha_compra': fecha_compra_str,
                'moneda': moneda,
                'proveedores': proveedores,
            }
            return render(request, 'Inventario/form_compra.html', context)
        
        # Validar que existe cotización para la fecha
        from flujo.models import CotizacionDolar
        if not CotizacionDolar.objects.filter(fecha=fecha_compra).exists():
            messages.error(
                request,
                f'No existe cotización del dólar para la fecha {fecha_compra.strftime("%d/%m/%Y")}. '
                'Por favor registre la cotización del día primero en el módulo de Flujo de Caja.'
            )
            formset = CompraInsumoDetalleFormSet(request.POST)
            from ProveedoresApp.models import Proveedores
            proveedores = Proveedores.objects.all().order_by('nombre')
            context = {
                'formset': formset,
                'accion': 'Registrar',
                'numero_factura': numero_factura,
                'fecha_compra': fecha_compra_str,
                'moneda': moneda,
                'proveedores': proveedores,
            }
            return render(request, 'Inventario/form_compra.html', context)
        
        formset = CompraInsumoDetalleFormSet(request.POST)
        
        if formset.is_valid():
            try:
                compras_creadas = []
                
                # Crear una CompraInsumo por cada línea del formset
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        # Verificar que los campos obligatorios tengan valores
                        insumo = form.cleaned_data.get('insumo')
                        cantidad = form.cleaned_data.get('cantidad')
                        monto = form.cleaned_data.get('monto')
                        
                        # Solo procesar si todos los campos obligatorios tienen valores
                        if insumo and cantidad and monto:
                            compra = CompraInsumo(
                                numero_factura=numero_factura,
                                fecha_compra=fecha_compra,
                                moneda=moneda,
                                aplicar_iva=form.cleaned_data.get('aplicar_iva', False),  # IVA por item
                                insumo=insumo,
                                cantidad=cantidad,
                                monto=monto,
                            )
                            print(f"🔵 Antes de guardar CompraInsumo: {compra.insumo}")
                            compra.save()
                            print(f"🟢 Después de guardar CompraInsumo ID: {compra.pk}")
                            compras_creadas.append(compra)
                
                if not compras_creadas:
                    messages.error(request, 'Debe agregar al menos un insumo.')
                    from ProveedoresApp.models import Proveedores
                    proveedores = Proveedores.objects.all().order_by('nombre')
                    context = {
                        'formset': formset,
                        'accion': 'Registrar',
                        'numero_factura': numero_factura,
                        'fecha_compra': fecha_compra_str,
                        'moneda': moneda,
                        'proveedores': proveedores,
                    }
                    return render(request, 'Inventario/form_compra.html', context)
                
                total_compras = len(compras_creadas)
                total_usd = sum(c.monto_total_usd for c in compras_creadas)
                
                messages.success(
                    request,
                    f'Se registraron {total_compras} compra(s) exitosamente. Total: ${total_usd:.2f} USD'
                )
                return redirect('listar_compras')
            except ValidationError as e:
                messages.error(request, f'Error de validación: {e}')
                from ProveedoresApp.models import Proveedores
                proveedores = Proveedores.objects.all().order_by('nombre')
                context = {
                    'formset': formset,
                    'accion': 'Registrar',
                    'numero_factura': numero_factura,
                    'fecha_compra': fecha_compra_str,
                    'moneda': moneda,
                    'proveedores': proveedores,
                }
                return render(request, 'Inventario/form_compra.html', context)
            except Exception as e:
                messages.error(request, f'Error al registrar las compras: {str(e)}')
                from ProveedoresApp.models import Proveedores
                proveedores = Proveedores.objects.all().order_by('nombre')
                context = {
                    'formset': formset,
                    'accion': 'Registrar',
                    'numero_factura': numero_factura,
                    'fecha_compra': fecha_compra_str,
                    'moneda': moneda,
                    'proveedores': proveedores,
                }
                return render(request, 'Inventario/form_compra.html', context)
        else:
            messages.error(request, f'Errores en el formulario: {formset.errors}')
            from ProveedoresApp.models import Proveedores
            proveedores = Proveedores.objects.all().order_by('nombre')
            context = {
                'formset': formset,
                'accion': 'Registrar',
                'numero_factura': numero_factura,
                'fecha_compra': fecha_compra_str,
                'moneda': moneda,
                'proveedores': proveedores,
            }
            return render(request, 'Inventario/form_compra.html', context)
    else:
        formset = CompraInsumoDetalleFormSet()
    
    # Obtener proveedores para el modal
    from ProveedoresApp.models import Proveedores
    proveedores = Proveedores.objects.all().order_by('nombre')
    
    context = {
        'formset': formset,
        'accion': 'Registrar',
        'proveedores': proveedores,
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
    return render(request, 'Inventario/form_compra_editar.html', context)


@login_required
def anular_compra(request, pk):
    """Anula una compra individual (reemplaza eliminar_compra)"""
    compra = get_object_or_404(CompraInsumo, pk=pk)
    
    if compra.anulada:
        messages.warning(request, 'Esta compra ya está anulada.')
        return redirect('listar_compras')
    
    if request.method == 'POST':
        try:
            compra.anular()
            messages.success(request, f'Compra anulada exitosamente. Se ha creado un movimiento de reversa en el flujo de caja.')
            return redirect('listar_compras')
        except Exception as e:
            messages.error(request, f'Error al anular la compra: {str(e)}')
    
    context = {
        'compra': compra,
    }
    return render(request, 'Inventario/anular_compra.html', context)



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
        # Obtener filtros de fecha
        fecha_desde = request.GET.get('fecha_desde', '')
        fecha_hasta = request.GET.get('fecha_hasta', '')
        
        # Filtrar compras
        compras = CompraInsumo.objects.all()
        
        if fecha_desde:
            compras = compras.filter(fecha_compra__gte=fecha_desde)
        if fecha_hasta:
            compras = compras.filter(fecha_compra__lte=fecha_hasta)
        
        # Agrupar por número de factura (igual que en listar_compras)
        compras_agrupadas = []
        facturas_procesadas = set()
        
        for compra in compras.order_by('-fecha_compra', 'numero_factura'):
            # Crear una clave única para agrupar (numero_factura + fecha)
            clave = f"{compra.numero_factura or 'SIN_FACTURA'}_{compra.fecha_compra}"
            
            if clave not in facturas_procesadas:
                facturas_procesadas.add(clave)
                
                # Obtener todas las compras con el mismo numero_factura y fecha
                if compra.numero_factura:
                    items = CompraInsumo.objects.filter(
                        numero_factura=compra.numero_factura,
                        fecha_compra=compra.fecha_compra
                    )
                else:
                    # Si no tiene número de factura, solo agrupar esta compra individual
                    items = CompraInsumo.objects.filter(pk=compra.pk)
                
                # Calcular totales del grupo
                total_bs = sum(item.monto_total_bs or 0 for item in items)
                total_usd = sum(item.monto_total_usd or 0 for item in items)
                subtotal_bs = sum(item.monto_bs or 0 for item in items)
                subtotal_usd = sum(item.monto_usd or 0 for item in items)
                
                # Verificar si todas las compras están anuladas
                todas_anuladas = all(item.anulada for item in items)
                
                compras_agrupadas.append({
                    'numero_factura': compra.numero_factura or '-',
                    'fecha_compra': compra.fecha_compra,
                    'moneda': compra.moneda,
                    'aplicar_iva': compra.aplicar_iva,
                    'cantidad_items': items.count(),
                    'subtotal_bs': subtotal_bs,
                    'subtotal_usd': subtotal_usd,
                    'total_bs': total_bs,
                    'total_usd': total_usd,
                    'anulada': todas_anuladas,
                })
        
        # Calcular totales generales (excluyendo anuladas)
        total_facturas = len([g for g in compras_agrupadas if not g['anulada']])
        total_bs_general = sum(g['total_bs'] for g in compras_agrupadas if not g['anulada'])
        total_usd_general = sum(g['total_usd'] for g in compras_agrupadas if not g['anulada'])
        
        html_string = render_to_string('Inventario/compras_pdf.html', {
            'compras_agrupadas': compras_agrupadas,
            'total_facturas': total_facturas,
            'total_bs': total_bs_general,
            'total_usd': total_usd_general,
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


@login_required
def compras_detallado_pdf(request):
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from weasyprint import HTML, CSS
    from django.conf import settings
    from decimal import Decimal
    import os
    import traceback
    import datetime

    try:
        # Obtener filtros de fecha
        fecha_desde = request.GET.get('fecha_desde', '')
        fecha_hasta = request.GET.get('fecha_hasta', '')
        insumo_filtro = request.GET.get('insumo', '')
        
        # Filtrar compras
        compras = CompraInsumo.objects.all().order_by('-fecha_compra', 'numero_factura')
        
        if fecha_desde:
            compras = compras.filter(fecha_compra__gte=fecha_desde)
        if fecha_hasta:
            compras = compras.filter(fecha_compra__lte=fecha_hasta)
        if insumo_filtro:
            compras = compras.filter(insumo__descripcion__icontains=insumo_filtro)
        
        # Calcular totales generales (excluyendo anuladas)
        total_compras = compras.filter(anulada=False).count()
        total_bs_general = sum(c.monto_total_bs or 0 for c in compras if not c.anulada)
        total_usd_general = sum(c.monto_total_usd or 0 for c in compras if not c.anulada)
        
        html_string = render_to_string('Inventario/compras_detallado_pdf.html', {
            'compras': compras,
            'total_compras': total_compras,
            'total_bs': total_bs_general,
            'total_usd': total_usd_general,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'insumo_filtro': insumo_filtro,
            'fecha_generacion': datetime.date.today(),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="listado_compras_detallado.pdf"'

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
    """Lista todos los usos de insumos con filtros opcionales"""
    # Obtener filtros
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    descripcion_filtro = request.GET.get('descripcion', '')
    
    # Filtrar usos
    usos = UsoInsumo.objects.all().order_by('-fecha_uso')
    
    if fecha_desde:
        usos = usos.filter(fecha_uso__gte=fecha_desde)
    if fecha_hasta:
        usos = usos.filter(fecha_uso__lte=fecha_hasta)
    if descripcion_filtro:
        usos = usos.filter(descripcion__icontains=descripcion_filtro)
    
    context = {
        'usos': usos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'descripcion_filtro': descripcion_filtro,
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


@login_required
def usos_pdf(request):
    """Genera PDF del listado de uso de insumos con filtros opcionales"""
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from weasyprint import HTML, CSS
    from django.conf import settings
    from decimal import Decimal
    import os
    import traceback
    import datetime

    try:
        # Obtener filtros
        fecha_desde = request.GET.get('fecha_desde', '')
        fecha_hasta = request.GET.get('fecha_hasta', '')
        descripcion_filtro = request.GET.get('descripcion', '')
        
        # Filtrar usos
        usos = UsoInsumo.objects.all().order_by('-fecha_uso')
        
        if fecha_desde:
            usos = usos.filter(fecha_uso__gte=fecha_desde)
        if fecha_hasta:
            usos = usos.filter(fecha_uso__lte=fecha_hasta)
        if descripcion_filtro:
            usos = usos.filter(descripcion__icontains=descripcion_filtro)
        
        # Calcular totales
        total_usos = usos.count()
        total_costo_usd = sum(uso.costo_total_usd or Decimal('0') for uso in usos)
        
        html_string = render_to_string('Inventario/usos_pdf.html', {
            'usos': usos,
            'total_usos': total_usos,
            'total_costo_usd': total_costo_usd,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'descripcion_filtro': descripcion_filtro,
            'fecha_generacion': datetime.date.today(),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="listado_usos_insumos.pdf"'

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


# ==================== VISTA AJAX PARA CREAR INSUMO ====================

@login_required
def crear_insumo_ajax(request):
    """Vista AJAX para crear un insumo rápidamente desde el formulario de compras"""
    from django.http import JsonResponse
    
    if request.method == 'POST':
        # Obtener datos del POST
        descripcion = request.POST.get('descripcion', '').strip()
        medida = request.POST.get('medida', '').strip()
        categoria = request.POST.get('categoria', '').strip()
        proveedor_id = request.POST.get('proveedor', '').strip()
        
        # Validar campos requeridos
        errors = {}
        
        if not descripcion:
            errors['descripcion'] = ['Este campo es requerido.']
        
        if not medida:
            errors['medida'] = ['Este campo es requerido.']
        elif medida not in dict(ExistenciaInsumo.MEDIDAS):
            errors['medida'] = ['Seleccione una opción válida.']
        
        if not categoria:
            errors['categoria'] = ['Este campo es requerido.']
        elif categoria not in dict(ExistenciaInsumo.CATEGORIA_CHOICES):
            errors['categoria'] = ['Seleccione una opción válida.']
        
        if not proveedor_id:
            errors['proveedor'] = ['Este campo es requerido.']
        else:
            from ProveedoresApp.models import Proveedores
            try:
                proveedor = Proveedores.objects.get(pk=proveedor_id)
            except Proveedores.DoesNotExist:
                errors['proveedor'] = ['Proveedor no válido.']
        
        # Verificar si ya existe un insumo con la misma descripción
        if descripcion and ExistenciaInsumo.objects.filter(descripcion__iexact=descripcion).exists():
            errors['descripcion'] = ['Ya existe un insumo con esta descripción.']
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        try:
            # Crear el insumo con valores por defecto
            insumo = ExistenciaInsumo(
                descripcion=descripcion,
                medida=medida,
                categoria=categoria,
                proveedor_id=proveedor_id,
                existencia=0,  # Valor por defecto
                existencia_minima=0,  # Valor por defecto
            )
            insumo.save()
            
            return JsonResponse({
                'success': True,
                'insumo': {
                    'id': insumo.pk,
                    'codigo': insumo.codigo,
                    'descripcion': insumo.descripcion,
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': {'general': [f'Error al crear el insumo: {str(e)}']}
            })
    
    return JsonResponse({'success': False, 'errors': {'general': ['Método no permitido.']}})


# ==================== IMPORTAR VISTAS DE COMPRAS AGRUPADAS ====================
from .views_grupo_compras import detalle_compra_grupo, editar_compra_grupo, anular_compra_grupo

