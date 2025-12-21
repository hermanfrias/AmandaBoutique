from django.urls import path
from LoginApp.views import *
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='LoginApp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='LoginApp/logout.html'), name='logout'),
    path('registrar/', registrar_usuario, name='registrar'),
    path('perfil/', perfil, name='perfil'),
    path('editar/', editar_perfil, name='editar_perfil'),
    path('gestionar-permisos/', gestionar_permisos, name='gestionar_permisos'),
    path('crear-usuario/', crear_usuario_admin, name='crear_usuario_admin'),
    path('editar-usuario/<int:user_id>/', editar_usuario_admin, name='editar_usuario_admin'),


    path('editar-permisos/<int:user_id>/', editar_permisos_usuario, name='editar_permisos_usuario'),
    path('eliminar-usuario/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
] 