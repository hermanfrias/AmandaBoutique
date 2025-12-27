from django.urls import path
from . import views

urlpatterns = [
    # Vestidos
    path('vestidos/', views.listar_vestidos, name='listar_vestidos'),
    path('vestidos/crear/', views.crear_vestido, name='crear_vestido'),
    path('vestidos/<int:pk>/', views.detalle_vestido, name='detalle_vestido'),
    path('vestidos/<int:pk>/editar/', views.editar_vestido, name='editar_vestido'),
    path('vestidos/<int:pk>/eliminar/', views.eliminar_vestido, name='eliminar_vestido'),
    
    # Alquileres
    path('', views.listar_alquileres, name='listar_alquileres'),
    path('crear/', views.crear_alquiler, name='crear_alquiler'),
    path('<int:pk>/', views.detalle_alquiler, name='detalle_alquiler'),
    path('<int:pk>/editar/', views.editar_alquiler, name='editar_alquiler'),
    path('<int:pk>/eliminar/', views.eliminar_alquiler, name='eliminar_alquiler'),
    path('<int:pk>/contrato/', views.generar_contrato_pdf, name='contrato_pdf'),
    
    # AJAX
    path('ajax/crear-cliente/', views.crear_cliente_rapido, name='crear_cliente_rapido'),
]
