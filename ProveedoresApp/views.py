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
