import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from weasyprint import HTML, CSS
from BoutiqueApp.forms import CatalogoForm
from BoutiqueApp.models import Catalogo
from Alquiler.models import Vestido


def index(request):
    catalogos = Catalogo.objects.all()
    # Mostrar solo vestidos activos para alquiler (excluir Dañado, Vendido y Baja)
    vestidos_alquiler = Vestido.objects.exclude(
        estado__in=['Dañado', 'Vendido', 'Baja']
    ).order_by('-fecha_creacion')
    return render(request, 'BoutiqueApp/index.html', {
        'catalogos': catalogos,
        'vestidos_alquiler': vestidos_alquiler
    })

@login_required
@permission_required('BoutiqueApp.add_catalogo', raise_exception=True)
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

def detalle_catalogo(request, codigo):
    catalogo = Catalogo.objects.get(codigo=codigo)
    return render(request, 'BoutiqueApp/detalle_catalogo.html', {'catalogo': catalogo})

# --- EDITAR LOS REGISTROS ---

@login_required
@permission_required('BoutiqueApp.change_catalogo', raise_exception=True)
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
@permission_required('BoutiqueApp.delete_catalogo', raise_exception=True)
def eliminar_catalogo(request, codigo):
    catalogo = Catalogo.objects.get(codigo=codigo)
    if request.method == 'POST':
        # Eliminar la imagen del sistema de archivos si existe
        if catalogo.imagen_modelo:
            try:
                # Construir la ruta completa del archivo
                imagen_path = os.path.join(settings.MEDIA_ROOT, str(catalogo.imagen_modelo))
                # Verificar si el archivo existe y eliminarlo
                if os.path.exists(imagen_path):
                    os.remove(imagen_path)
                    
                    # Intentar eliminar la carpeta padre si está vacía
                    carpeta_padre = os.path.dirname(imagen_path)
                    try:
                        if os.path.exists(carpeta_padre) and not os.listdir(carpeta_padre):
                            os.rmdir(carpeta_padre)
                    except OSError:
                        pass  # La carpeta no está vacía o no se puede eliminar
            except Exception as e:
                # Log del error pero continuar con la eliminación del registro
                print(f"Error al eliminar imagen: {e}")
        
        # Eliminar el registro de la base de datos
        catalogo.delete()
        messages.success(request, 'Producto eliminado correctamente junto con su imagen')
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

@login_required
def catalogo_alquiler_pdf(request):
    """Genera PDF del catálogo de vestidos de alquiler en formato lista"""
    vestidos = Vestido.objects.filter(estado='Disponible').order_by('nombre_modelo')

    # Renderizamos HTML
    html_string = render_to_string('BoutiqueApp/catalogo_alquiler_pdf.html', {
        'vestidos': vestidos
    })

    # Creamos respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="catalogo_alquiler_amanda_boutique.pdf"'

    # Ruta del CSS para estilos PDF
    css_path = os.path.join(settings.STATICFILES_DIRS[0], "BoutiqueApp/css/pdf.css")

    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        response, stylesheets=[CSS(css_path)]
    )
    return response

@login_required
def catalogo_alquiler_pdf_cards(request):
    """Genera PDF del catálogo de vestidos de alquiler en formato tarjetas"""
    vestidos = Vestido.objects.filter(estado='Disponible').order_by('nombre_modelo')
    html = render_to_string("BoutiqueApp/catalogo_alquiler_pdf_cards.html", {"vestidos": vestidos})
    
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'inline; filename="catalogo_alquiler_tarjetas_amanda_boutique.pdf"'

    css_path = os.path.join(settings.STATICFILES_DIRS[0], "BoutiqueApp/css/catalog_cards.css")

    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
        response,
        stylesheets=[CSS(css_path)]
    )

    return response

