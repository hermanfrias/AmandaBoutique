from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_movimientos, name='listar_movimientos'),
    path('movimientos/crear/', views.crear_movimiento, name='crear_movimiento'),
    path('movimientos/editar/<int:id>/', views.editar_movimiento, name='editar_movimiento'),
    path('movimientos/ver/<int:id>/', views.ver_movimiento, name='ver_movimiento'),
    path('movimientos/eliminar/<int:id>/', views.eliminar_movimiento, name='eliminar_movimiento'),
    path('movimientos/pdf/', views.movimientos_pdf, name='movimientos_pdf'),
    path('movimientos/excel/', views.movimientos_excel, name='movimientos_excel'),
    path('cotizaciones/', views.listar_cotizaciones, name='listar_cotizaciones'),
    path('cotizaciones/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('cotizaciones/editar/<int:id>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('cotizaciones/eliminar/<int:id>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('configuraciones-iva/', views.listar_configuraciones_iva, name='listar_configuraciones_iva'),
    path('configuraciones-iva/crear/', views.crear_configuracion_iva, name='crear_configuracion_iva'),
    path('configuraciones-iva/editar/<int:id>/', views.editar_configuracion_iva, name='editar_configuracion_iva'),
    path('configuraciones-iva/eliminar/<int:id>/', views.eliminar_configuracion_iva, name='eliminar_configuracion_iva'),
    path('dashboard/', views.dashboard_flujo, name='dashboard_flujo'),
]
