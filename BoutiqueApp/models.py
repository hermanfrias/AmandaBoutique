from django.db import models

class Catalogo(models.Model):
    codigo = models.CharField(max_length=20, unique=True, blank=True)
    modelo = models.CharField(max_length=100)
    estilo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_modelo = models.ImageField(upload_to='imagenes', null=True, verbose_name='Foto 1')
    foto2 = models.ImageField(upload_to='imagenes', null=True, blank=True, verbose_name='Foto 2')
    foto3 = models.ImageField(upload_to='imagenes', null=True, blank=True, verbose_name='Foto 3')
    foto4 = models.ImageField(upload_to='imagenes', null=True, blank=True, verbose_name='Foto 4')

    def save(self, *args, **kwargs):
        if not self.codigo:  # Si no tiene código, lo generamos
            # Intentamos generar un código único
            while True:
                try:
                    ultimo = Catalogo.objects.all().order_by('codigo').last()
                    if not ultimo:
                        nuevo_codigo = 'CAT00001'
                    else:
                        # Extraemos el número, manejando posibles errores de formato
                        try:
                            num = int(ultimo.codigo.replace('CAT', '')) + 1
                        except ValueError:
                            # Si el último código no tiene el formato esperado, forzamos uno nuevo o usamos timestamp
                            # Para mantener consistencia simple:
                            num = 1 
                        nuevo_codigo = "CAT" + f"{num:05d}"
                    
                    self.codigo = nuevo_codigo
                    super().save(*args, **kwargs)
                    break # Éxito, salimos del loop
                except Exception as e:
                    # Si hay error de integridad (código duplicado por carrera), reintentamos
                    # Nota: En un entorno de alta concurrencia, esto debería mejorarse.
                    if 'unique constraint' in str(e).lower() or 'integrity' in str(e).lower():
                        continue
                    raise e
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo}: {self.modelo} - {self.estilo}"




# ============================================
# SIGNALS PARA ELIMINAR FOTOS AUTOMÁTICAMENTE
# ============================================

import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

@receiver(post_delete, sender=Catalogo)
def auto_delete_catalogo_photos_on_delete(sender, instance, **kwargs):
    '''Elimina las fotos del sistema de archivos cuando se elimina un Catalogo'''
    for field_name in ['imagen_modelo', 'foto2', 'foto3', 'foto4']:
        field = getattr(instance, field_name)
        if field:
            if os.path.isfile(field.path):
                try:
                    os.remove(field.path)
                except Exception as e:
                    print(f'Error al eliminar {field_name}: {e}')

@receiver(pre_save, sender=Catalogo)
def auto_delete_catalogo_photos_on_change(sender, instance, **kwargs):
    '''Elimina la foto antigua cuando se reemplaza por una nueva'''
    if not instance.pk:
        return False

    try:
        old_instance = Catalogo.objects.get(pk=instance.pk)
    except Catalogo.DoesNotExist:
        return False

    for field_name in ['imagen_modelo', 'foto2', 'foto3', 'foto4']:
        old_field = getattr(old_instance, field_name)
        new_field = getattr(instance, field_name)
        
        if old_field and old_field != new_field:
            if os.path.isfile(old_field.path):
                try:
                    os.remove(old_field.path)
                except Exception as e:
                    print(f'Error al eliminar {field_name} antigua: {e}')
