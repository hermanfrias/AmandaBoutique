from ClientesApp.forms import ClientesForm
from ClientesApp.models import Clientes
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

class ClientesListView(LoginRequiredMixin, ListView):
    model = Clientes
    template_name = 'ClientesApp/clientes_list.html'
    context_object_name = 'clientes'
    
    def get_queryset(self):
        query = self.request.GET.get('buscar', '')
        if query:
            return Clientes.objects.filter(nombre__icontains=query)
        return Clientes.objects.all()

class ClientesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'ClientesApp.add_clientes'
    model = Clientes
    form_class = ClientesForm
    template_name = 'ClientesApp/clientes_create.html'
    success_url = reverse_lazy('clientes_list')  

class ClientesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'ClientesApp.change_clientes'
    model = Clientes
    form_class = ClientesForm
    template_name = 'ClientesApp/clientes_update.html'
    success_url = reverse_lazy('clientes_list')
    slug_field = "identificacion"
    slug_url_kwarg = "identificacion"

class ClientesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'ClientesApp.delete_clientes'
    model = Clientes
    template_name = 'ClientesApp/clientes_confirm_delete.html'
    success_url = reverse_lazy('clientes_list')
    slug_field = "identificacion"
    slug_url_kwarg = "identificacion"
    
class ClientesDetailView(LoginRequiredMixin, DetailView):
    model = Clientes
    template_name = "ClientesApp/clientes_detail.html"
    context_object_name = "clientes"
    slug_field = "identificacion"
    slug_url_kwarg = "identificacion"


@login_required
def clientes_pdf(request):
    """Genera PDF del listado de clientes con filtro opcional de búsqueda"""
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from weasyprint import HTML, CSS
    from django.conf import settings
    import os
    import traceback
    import datetime

    try:
        # Obtener filtro de búsqueda
        buscar = request.GET.get('buscar', '')
        
        # Filtrar clientes
        clientes = Clientes.objects.all().order_by('apellido', 'nombre')
        
        if buscar:
            clientes = clientes.filter(nombre__icontains=buscar)
        
        # Calcular totales
        total_clientes = clientes.count()
        
        html_string = render_to_string('ClientesApp/clientes_pdf.html', {
            'clientes': clientes,
            'total_clientes': total_clientes,
            'buscar': buscar,
            'fecha_generacion': datetime.date.today(),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="listado_clientes.pdf"'

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
