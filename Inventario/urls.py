from django.urls import path
from . import views
from .views_activos_fijos import (
    listar_activos, crear_activo, editar_activo, detalle_activo,
    eliminar_activo, registrar_mantenimiento, activos_pdf
)

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
    path('compras/detallado/', views.listar_compras_detallado, name='listar_compras_detallado'),
    path('compras/crear/', views.crear_compra, name='crear_compra'),
    path('compras/<int:pk>/editar/', views.editar_compra, name='editar_compra'),
    path('compras/<int:pk>/detalle/', views.detalle_compra, name='detalle_compra'),
    path('compras/<int:pk>/anular/', views.anular_compra, name='anular_compra'),
    
    # URLs para operaciones agrupadas por factura
    path('compras/grupo/<str:numero_factura>/<str:fecha>/detalle/', views.detalle_compra_grupo, name='detalle_compra_grupo'),
    path('compras/grupo/<str:numero_factura>/<str:fecha>/editar/', views.editar_compra_grupo, name='editar_compra_grupo'),
    path('compras/grupo/<str:numero_factura>/<str:fecha>/anular/', views.anular_compra_grupo, name='anular_compra_grupo'),
    path('compras/pdf/', views.compras_pdf, name='compras_pdf'),
    path('compras/detallado/pdf/', views.compras_detallado_pdf, name='compras_detallado_pdf'),
    
    # URLs para UsoInsumo
    path('usos/', views.listar_usos, name='listar_usos'),
    path('usos/crear/', views.crear_uso, name='crear_uso'),
    path('usos/<int:pk>/editar/', views.editar_uso, name='editar_uso'),
    path('usos/<int:pk>/', views.detalle_uso, name='detalle_uso'),
    path('usos/<int:pk>/eliminar/', views.eliminar_uso, name='eliminar_uso'),
    path('usos/pdf/', views.usos_pdf, name='usos_pdf'),
    
    # URLs para Activos Fijos
    path('activos/', listar_activos, name='listar_activos'),
    path('activos/crear/', crear_activo, name='crear_activo'),
    path('activos/<str:numero_inventario>/', detalle_activo, name='detalle_activo'),
    path('activos/<str:numero_inventario>/editar/', editar_activo, name='editar_activo'),
    path('activos/<str:numero_inventario>/eliminar/', eliminar_activo, name='eliminar_activo'),
    path('activos/<str:numero_inventario>/mantenimiento/', registrar_mantenimiento, name='registrar_mantenimiento'),
    path('activos/pdf/export/', activos_pdf, name='activos_pdf'),
]
