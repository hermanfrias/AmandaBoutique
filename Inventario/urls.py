from django.urls import path
from . import views

urlpatterns = [
    # URLs para ExistenciaInsumo
    path('insumos/', views.listar_insumos, name='listar_insumos'),
    path('insumos/crear/', views.crear_insumo, name='crear_insumo'),
    path('insumos/<int:pk>/editar/', views.editar_insumo, name='editar_insumo'),
    path('insumos/<int:pk>/eliminar/', views.eliminar_insumo, name='eliminar_insumo'),
    path('insumos/<int:pk>/', views.detalle_insumo, name='detalle_insumo'),
    path('insumos/pdf/', views.insumos_pdf, name='insumos_pdf'),
    
    # URLs para CompraInsumo
    path('compras/', views.listar_compras, name='listar_compras'),
    path('compras/crear/', views.crear_compra, name='crear_compra'),
    path('compras/<int:pk>/editar/', views.editar_compra, name='editar_compra'),
    path('compras/<int:pk>/eliminar/', views.eliminar_compra, name='eliminar_compra'),
    path('compras/<int:pk>/', views.detalle_compra, name='detalle_compra'),
    path('compras/pdf/', views.compras_pdf, name='compras_pdf'),
    
    # URLs para UsoInsumo
    path('usos/', views.listar_usos, name='listar_usos'),
    path('usos/crear/', views.crear_uso, name='crear_uso'),
    path('usos/<int:pk>/editar/', views.editar_uso, name='editar_uso'),
    path('usos/<int:pk>/', views.detalle_uso, name='detalle_uso'),
    path('usos/<int:pk>/eliminar/', views.eliminar_uso, name='eliminar_uso'),
]
