from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cita
from .forms import CitaForm
from django.contrib import messages
from django.http import JsonResponse

@login_required
def listar_citas(request):
    # Búsqueda por cliente
    query = request.GET.get('buscar', '')
    citas = Cita.objects.all()
    
    if query:
        citas = citas.filter(cliente__icontains=query)

    # Orden dinámico por GET
    orden = request.GET.get('orden', '')
    if orden == "fecha":
        citas = citas.order_by("fecha")
    elif orden == "-fecha":
        citas = citas.order_by("-fecha")
    elif orden == "entrega":
        citas = citas.order_by("fecha_entrega")
    elif orden == "-entrega":
        citas = citas.order_by("-fecha_entrega")
    else:
        citas = citas.order_by("cliente")  # Orden por defecto

    return render(request, 'citas/listar_citas.html', {'citas': citas})


@login_required
def crear_cita(request):
    if request.method=='POST':
        form=CitaForm(request.POST)
        if form.is_valid():
            cita=form.save(commit=False)
            cita.creado_por=request.user
            cita.save()
            messages.success(request,"Cita creada correctamente")
            return redirect('listar_citas')
    else:
        form=CitaForm()
    return render(request,'citas/crear_cita.html',{'form':form})

@login_required
def editar_cita(request, pk):
    cita=get_object_or_404(Cita, pk=pk)
    if request.method=='POST':
        form=CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request,"Cita actualizada correctamente")
            return redirect('listar_citas')
    else:
        form=CitaForm(instance=cita)
    return render(request,'citas/editar_cita.html',{'form':form})

@login_required
def eliminar_cita(request, pk):
    cita=get_object_or_404(Cita, pk=pk)
    if request.method=='POST':
        cita.delete()
        return redirect('listar_citas')
    return render(request,'citas/eliminar_cita.html',{'cita':cita})

def ver_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    return render(request, 'citas/ver_cita.html', {'cita': cita})

@login_required
def calendario_citas(request):
    return render(request, 'citas/calendario.html')


@login_required
def eventos_citas(request):
    from django.urls import reverse
    
    citas = Cita.objects.all()
    eventos = []
    for c in citas:
        # Evento de fecha de cita (color rosa)
        hora_12 = c.hora.strftime("%I:%M %p") if c.hora else ""
        eventos.append({
            "title": f"{hora_12} - {c.cliente} - {c.get_accion_display()}",
            "start": str(c.fecha),
            "color": "#E91E63",
            "allDay": True,
            "url": reverse("ver_cita", args=[c.pk])  # 👈
        })

        # Evento de fecha de entrega (color morado)
        if c.fecha_entrega:
            eventos.append({
                "title": f"Entrega: {c.cliente}",
                "start": str(c.fecha_entrega),
                "color": "#6A1B9A",
                "allDay": True,
                "url": reverse("ver_cita", args=[c.pk])  # 👈
            })

    return JsonResponse(eventos, safe=False)

@login_required
def citas_pdf(request):
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from weasyprint import HTML, CSS
    from django.conf import settings
    import os

    from django.utils.dateparse import parse_date
    from django.db.models import Q

    citas = Cita.objects.all().order_by('fecha_entrega', 'fecha')

    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    fecha_inicio = parse_date(fecha_inicio_str) if fecha_inicio_str else None
    fecha_fin = parse_date(fecha_fin_str) if fecha_fin_str else None

    if fecha_inicio and fecha_fin:
        citas = citas.filter(
            Q(fecha__range=[fecha_inicio, fecha_fin]) |
            Q(fecha_entrega__range=[fecha_inicio, fecha_fin])
        )
    elif fecha_inicio:
        citas = citas.filter(
            Q(fecha__gte=fecha_inicio) |
            Q(fecha_entrega__gte=fecha_inicio)
        )
    elif fecha_fin:
        citas = citas.filter(
            Q(fecha__lte=fecha_fin) |
            Q(fecha_entrega__lte=fecha_fin)
        )
    
    html_string = render_to_string('citas/citas_pdf.html', {
        'citas': citas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_citas.pdf"'

    # Ruta del CSS para estilos PDF (reutilizamos el de BoutiqueApp o uno específico si se creó)
    css_path = os.path.join(settings.STATICFILES_DIRS[0], "BoutiqueApp/css/pdf.css")

    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[CSS(css_path)]
    )
    return response
