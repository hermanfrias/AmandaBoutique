from ClientesApp.forms import ClientesForm
from ClientesApp.models import Clientes
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
