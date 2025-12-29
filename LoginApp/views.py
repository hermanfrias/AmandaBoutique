from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from LoginApp.froms import FormularioCreacionUsuario, FormularioCambioUsuario

def registrar_usuario(request):
    if request.method == 'POST':
        form = FormularioCreacionUsuario(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Asignar solo permisos de lectura (view) a nuevos usuarios
            from django.contrib.contenttypes.models import ContentType
            from django.contrib.auth.models import Permission
            
            # Lista de modelos para asignar permisos de view
            models_to_grant_view = [
                ('BoutiqueApp', 'catalogo'),
                ('citas', 'cita'),
                ('ClientesApp', 'cliente'),
                ('ProveedoresApp', 'proveedor'),
                ('flujo', 'movimientocaja'),
                ('flujo', 'cotizaciondolar'),
            ]
            
            for app_label, model_name in models_to_grant_view:
                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                    view_permission = Permission.objects.get(
                        content_type=content_type,
                        codename=f'view_{model_name}'
                    )
                    user.user_permissions.add(view_permission)
                except (ContentType.DoesNotExist, Permission.DoesNotExist):
                    pass  # Si el modelo no existe, continuar
            
            login(request, user)
            return redirect('perfil')
    else:
        form = FormularioCreacionUsuario()
    return render(request, 'LoginApp/registrar.html', {'form': form})

@login_required
def perfil(request):
    return(render(request, 'LoginApp/perfil.html', {'user':  request.user}))

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = FormularioCambioUsuario(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('editar_perfil')
    else:
        form = FormularioCambioUsuario(instance=request.user)
    return render(request, 'LoginApp/editar_perfil.html', {'form': form})


@login_required
def crear_usuario_admin(request):
    """Vista para que superusuarios creen nuevos usuarios"""
    if not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')
    
    if request.method == 'POST':
        form = FormularioCreacionUsuario(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Asignar solo permisos de lectura (view) a nuevos usuarios
            from django.contrib.contenttypes.models import ContentType
            from django.contrib.auth.models import Permission
            
            # Lista de modelos para asignar permisos de view
            models_to_grant_view = [
                ('BoutiqueApp', 'catalogo'),
                ('citas', 'cita'),
                ('ClientesApp', 'clientes'),
                ('ProveedoresApp', 'proveedores'),
                ('flujo', 'movimientocaja'),
                ('flujo', 'cotizaciondolar'),
            ]
            
            for app_label, model_name in models_to_grant_view:
                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                    view_permission = Permission.objects.get(
                        content_type=content_type,
                        codename=f'view_{model_name}'
                    )
                    user.user_permissions.add(view_permission)
                except (ContentType.DoesNotExist, Permission.DoesNotExist):
                    pass  # Si el modelo no existe, continuar
            
            from django.contrib import messages
            messages.success(request, f'Usuario {user.username} creado correctamente con permisos de lectura.')
            return redirect('gestionar_permisos')
    else:
        form = FormularioCreacionUsuario()
    return render(request, 'LoginApp/crear_usuario_admin.html', {'form': form})
@login_required

@login_required
def editar_usuario_admin(request, user_id):
    """Vista para que superusuarios editen usuarios"""
    if not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')
    
    from django.shortcuts import get_object_or_404
    from LoginApp.models import PerfilUsuario
    
    usuario = get_object_or_404(PerfilUsuario, id=user_id)
    
    # No permitir editar superusuarios
    if usuario.is_superuser:
        from django.contrib import messages
        messages.error(request, 'No se puede editar un superusuario.')
        return redirect('gestionar_permisos')
    
    if request.method == 'POST':
        form = FormularioCambioUsuario(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, f'Usuario {usuario.username} actualizado correctamente.')
            return redirect('gestionar_permisos')
    else:
        form = FormularioCambioUsuario(instance=usuario)
    
    return render(request, 'LoginApp/editar_usuario_admin.html', {'form': form, 'usuario': usuario})
def gestionar_permisos(request):
    """Vista para que superusuarios gestionen permisos de usuarios"""
    if not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')
    
    from LoginApp.models import PerfilUsuario
    usuarios = PerfilUsuario.objects.all().order_by('username')
    return render(request, 'LoginApp/gestionar_permisos.html', {'usuarios': usuarios})

@login_required
def editar_permisos_usuario(request, user_id):
    """Vista para editar permisos de un usuario específico"""
    if not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')
    
    from django.shortcuts import get_object_or_404
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    from LoginApp.models import PerfilUsuario
    
    usuario = get_object_or_404(PerfilUsuario, id=user_id)
    
    if request.method == 'POST':
        # Limpiar permisos actuales (excepto si es superusuario)
        if not usuario.is_superuser:
            usuario.user_permissions.clear()
            
            # Asignar nuevos permisos seleccionados
            permisos_seleccionados = request.POST.getlist('permisos')
            for permiso_id in permisos_seleccionados:
                try:
                    permiso = Permission.objects.get(id=permiso_id)
                    usuario.user_permissions.add(permiso)
                except Permission.DoesNotExist:
                    pass
        
        from django.contrib import messages
        messages.success(request, f'Permisos actualizados para {usuario.username}')
        return redirect('gestionar_permisos')
    
    # Obtener permisos organizados por modelo
    permisos_por_modelo = {}
    modelos = [
        # BoutiqueApp
        ('BoutiqueApp', 'catalogo', 'Catálogo'),
        
        # Alquiler
        ('Alquiler', 'vestido', 'Vestidos'),
        ('Alquiler', 'alquiler', 'Alquileres'),
        ('Alquiler', 'cliente', 'Clientes Alquiler'),
        
        # Citas
        ('citas', 'cita', 'Citas'),
        
        # Clientes
        ('ClientesApp', 'clientes', 'Clientes'),
        
        # Proveedores
        ('ProveedoresApp', 'proveedores', 'Proveedores'),
        
        # Flujo
        ('flujo', 'movimientocaja', 'Movimientos de Caja'),
        ('flujo', 'cotizaciondolar', 'Cotización Dólar'),
        
        # Inventario
        ('Inventario', 'insumo', 'Insumos'),
        ('Inventario', 'comprainsumo', 'Compras de Insumos'),
        ('Inventario', 'usoinsumo', 'Uso de Insumos'),
        ('Inventario', 'activofijo', 'Activos Fijos'),
        ('Inventario', 'mantenimientoactivo', 'Mantenimiento de Activos'),
        ('Inventario', 'configuracioniva', 'Configuración IVA'),
    ]
    
    for app_label, model_name, display_name in modelos:
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            permisos = Permission.objects.filter(content_type=content_type).order_by('codename')
            permisos_por_modelo[display_name] = permisos
        except ContentType.DoesNotExist:
            pass
    
    # Permisos actuales del usuario
    permisos_usuario = set(usuario.user_permissions.values_list('id', flat=True))
    
    context = {
        'usuario': usuario,
        'permisos_por_modelo': permisos_por_modelo,
        'permisos_usuario': permisos_usuario,
    }
    
    return render(request, 'LoginApp/editar_permisos.html', context)


@login_required
def eliminar_usuario(request, user_id):
    """Vista para eliminar un usuario"""
    if not request.user.is_superuser:
        from django.contrib import messages
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')
    
    import os
    from django.conf import settings
    from django.shortcuts import get_object_or_404
    from LoginApp.models import PerfilUsuario
    
    usuario = get_object_or_404(PerfilUsuario, id=user_id)
    
    # No permitir eliminar superusuarios
    if usuario.is_superuser:
        from django.contrib import messages
        messages.error(request, 'No se puede eliminar un superusuario.')
        return redirect('gestionar_permisos')
    
    if request.method == 'POST':
        username = usuario.username
        
        # Eliminar el avatar del sistema de archivos si existe y no es el default
        if usuario.avatar and str(usuario.avatar) != 'default/default_icono.png':
            try:
                # Construir la ruta completa del archivo
                avatar_path = os.path.join(settings.MEDIA_ROOT, str(usuario.avatar))
                # Verificar si el archivo existe y eliminarlo
                if os.path.exists(avatar_path):
                    os.remove(avatar_path)
                    
                    # Intentar eliminar la carpeta padre si está vacía
                    carpeta_padre = os.path.dirname(avatar_path)
                    try:
                        if os.path.exists(carpeta_padre) and not os.listdir(carpeta_padre):
                            os.rmdir(carpeta_padre)
                    except OSError:
                        pass  # La carpeta no está vacía o no se puede eliminar
            except Exception as e:
                # Log del error pero continuar con la eliminación del usuario
                print(f"Error al eliminar avatar: {e}")
        
        # Eliminar el usuario de la base de datos
        usuario.delete()
        from django.contrib import messages
        messages.success(request, f'Usuario {username} eliminado correctamente junto con su avatar.')
        return redirect('gestionar_permisos')
    
    return render(request, 'LoginApp/eliminar_usuario.html', {'usuario': usuario})
