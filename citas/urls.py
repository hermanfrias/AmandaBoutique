from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_citas, name='listar_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('editar/<int:pk>/', views.editar_cita, name='editar_cita'),
    path('eliminar/<int:pk>/', views.eliminar_cita, name='eliminar_cita'),

    path('citas/ver/<int:pk>/', views.ver_cita, name='ver_cita'),
    path('citas/', views.listar_citas, name='listar_citas'),
    path('citas/calendario/', views.calendario_citas, name='calendario_citas'),
    path('citas/api/', views.eventos_citas, name='eventos_citas'),
    path('citas/pdf/', views.citas_pdf, name='citas_pdf'),
    
]
