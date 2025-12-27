from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path("", index, name="index"),
    path('actualizar_catalogo/', views.actualizar_catalogo, name='actualizar_catalogo'),
    path('listar_catalogo/', views.listar_catalogo, name='listar_catalogo'),
    path('ver_catalogo/<str:codigo>/', views.detalle_catalogo, name='detalle_catalogo'),
    path('editar_catalogo/<str:codigo>/', views.editar_catalogo, name='editar_catalogo'),
    path('eliminar_catalogo/<str:codigo>/', views.eliminar_catalogo, name='eliminar_catalogo'),
    path('catalogo/pdf/', views.catalogo_pdf, name='catalogo_pdf'),
    path('catalogo/pdf/cards/', views.catalogo_pdf_cards, name='catalogo_pdf_cards'),
    path('catalogo-alquiler/pdf/', views.catalogo_alquiler_pdf, name='catalogo_alquiler_pdf'),
    path('catalogo-alquiler/pdf/cards/', views.catalogo_alquiler_pdf_cards, name='catalogo_alquiler_pdf_cards'),

]

