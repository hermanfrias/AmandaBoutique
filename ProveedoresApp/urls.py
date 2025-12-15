from django.urls import path
from ProveedoresApp import views

urlpatterns = [
    path('', views.ProveedoresListView.as_view(), name='proveedores_list'),
    path('create/', views.ProveedoresCreateView.as_view(), name='proveedores_create'),
    path('update/<slug:codigo_proveedor>/', views.ProveedoresUpdateView.as_view(), name='proveedores_update'),
    path('delete/<slug:codigo_proveedor>/', views.ProveedoresDeleteView.as_view(), name='proveedores_confirm_delete'),
    path('detail/<slug:codigo_proveedor>/', views.ProveedoresDetailView.as_view(), name='proveedores_detail'),
    path('pdf/', views.proveedores_pdf, name='proveedores_pdf'),
]
