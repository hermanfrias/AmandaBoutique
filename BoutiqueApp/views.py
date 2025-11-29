import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from weasyprint import HTML, CSS
from BoutiqueApp.forms import CatalogoForm
from BoutiqueApp.models import Catalogo


def index(request):
    catalogos = Catalogo.objects.all()
    return render(request, 'BoutiqueApp/index.html', {'catalogos': catalogos})

def actualizar_catalogo(request):
    if request.method == 'POST':
        form = CatalogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("actualizar_catalogo")
    else:
            form = CatalogoForm()
        
    return render(request, "BoutiqueApp/actualizar_catalogo.html", {'form': form})

# --- LISTAR BASES DE DATOS ---

@login_required
def listar_catalogo(request):
    query = request.GET.get('buscar', '')
    if len(query) > 0:
        catalogos = Catalogo.objects.filter(modelo__icontains=query).order_by('modelo')
    else:       
        catalogos = Catalogo.objects.all()
    return render(request, 'BoutiqueApp/listar_catalogo.html', {'catalogos': catalogos})

# --- VER DETALLES DE LOS REGISTROS ---

@login_required
def detalle_catalogo(request, codigo):
    catalogo = Catalogo.objects.get(codigo=codigo)
    return render(request, 'BoutiqueApp/detalle_catalogo.html', {'catalogo': catalogo})

# --- EDITAR LOS REGISTROS ---

@login_required
def editar_catalogo(request, codigo):
    catalogo = Catalogo.objects.get(codigo=codigo)
    if request.method == 'POST':
        form = CatalogoForm(request.POST, request.FILES, instance=catalogo )
        if form.is_valid():
            form.save()
            return redirect('listar_catalogo')
    else:
        form = CatalogoForm(instance=catalogo)
    return render(request, 'BoutiqueApp/editar_catalogo.html', {'form': form})

# --- ELIMINAR UN REGISTROS ---

@login_required
def eliminar_catalogo(request, codigo):
    catalogo = Catalogo.objects.get(codigo=codigo)
    if request.method == 'POST':
        catalogo.delete()
        return redirect('listar_catalogo')
    return render(request, 'BoutiqueApp/eliminar_catalogo.html', {'catalogo': catalogo})

@login_required
def catalogo_pdf(request):
    catalogos = Catalogo.objects.all()

    # Renderizamos HTML
    html_string = render_to_string('BoutiqueApp/catalogo_pdf.html', {
        'catalogos': catalogos
    })

    # Creamos respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="catalogo_amanda_boutique.pdf"'

    # Ruta del CSS para estilos PDF
    css_path = os.path.join(settings.STATICFILES_DIRS[0], "BoutiqueApp/css/pdf.css")

    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[CSS(css_path)]
    )
    return response

@login_required
def catalogo_pdf_cards(request):
    catalogos = Catalogo.objects.all()
    html = render_to_string("BoutiqueApp/catalogo_pdf_cards.html", {"catalogos": catalogos})
    
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'inline; filename="catalogo_tarjetas_amanda_boutique.pdf"'

    css_path = os.path.join(settings.STATICFILES_DIRS[0], "BoutiqueApp/css/catalog_cards.css")

    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[CSS(css_path)]
    )

    return response

