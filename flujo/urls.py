from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_movimientos, name='listar_movimientos'),
    path('movimientos/crear/', views.crear_movimiento, name='crear_movimiento'),
    path('movimientos/pdf/', views.movimientos_pdf, name='movimientos_pdf'),
    path('movimientos/excel/', views.movimientos_excel, name='movimientos_excel'),
    path('cotizaciones/', views.listar_cotizaciones, name='listar_cotizaciones'),
    path('cotizaciones/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('cotizaciones/editar/<int:id>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('cotizaciones/eliminar/<int:id>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('dashboard/', views.dashboard_flujo, name='dashboard_flujo'),
]