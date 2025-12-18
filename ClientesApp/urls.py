from django.urls import path
from ClientesApp.views import *

urlpatterns = [
    path('', ClientesListView.as_view(), name='clientes_list'),
    path('pdf/export/', clientes_pdf, name='clientes_pdf'),
    path('crear/', ClientesCreateView.as_view(), name='clientes_create'),
    path('<str:identificacion>/editar/', ClientesUpdateView.as_view(), name='clientes_update'),
    path('<str:identificacion>/eliminar/', ClientesDeleteView.as_view(), name='clientes_confirm_delete'),
    path('<str:identificacion>/', ClientesDetailView.as_view(), name='clientes_detail'),
]
