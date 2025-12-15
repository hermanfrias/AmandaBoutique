from ProveedoresApp.forms import ProveedorForm
from ProveedoresApp.models import Proveedores
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

class ProveedoresListView(LoginRequiredMixin, ListView):
    model = Proveedores
    template_name = 'ProveedoresApp/proveedores_list.html'
    context_object_name = 'proveedores'
    
    def get_queryset(self):
        query = self.request.GET.get('buscar', '')
        if query:
            return Proveedores.objects.filter(nombre__icontains=query)
        return Proveedores.objects.all()

class ProveedoresCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'ProveedoresApp.add_proveedores'
    model = Proveedores
    form_class = ProveedorForm
    template_name = 'ProveedoresApp/proveedores_create.html'
    success_url = reverse_lazy('proveedores_list')  

class ProveedoresUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'ProveedoresApp.change_proveedores'
    model = Proveedores
    form_class = ProveedorForm
    template_name = 'ProveedoresApp/proveedores_update.html'
    success_url = reverse_lazy('proveedores_list')
    slug_field = "codigo_proveedor"
    slug_url_kwarg = "codigo_proveedor"

class ProveedoresDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'ProveedoresApp.delete_proveedores'
    model = Proveedores
    template_name = 'ProveedoresApp/proveedores_confirm_delete.html'
    success_url = reverse_lazy('proveedores_list')
    slug_field = "codigo_proveedor"
    slug_url_kwarg = "codigo_proveedor"
    
class ProveedoresDetailView(LoginRequiredMixin, DetailView):
    model = Proveedores
    template_name = "ProveedoresApp/proveedores_detail.html"
    context_object_name = "proveedores"
    slug_field = "codigo_proveedor"
    slug_url_kwarg = "codigo_proveedor"


# ==================== VISTA PARA PDF DE PROVEEDORES ====================

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.conf import settings
import os
import traceback
import datetime

@login_required
def proveedores_pdf(request):
    try:
        proveedores = Proveedores.objects.all().order_by('nombre')
        
        # Calcular totales
        total_proveedores = proveedores.count()
        
        html_string = render_to_string('ProveedoresApp/proveedores_pdf.html', {
            'proveedores': proveedores,
            'total_proveedores': total_proveedores,
            'fecha_generacion': datetime.date.today(),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="listado_proveedores.pdf"'

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
