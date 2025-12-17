from django.apps import AppConfig


class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Inventario'
    
    def ready(self):
        # Importar las señales para que se registren
        print("🚀 Cargando signals de Inventario...")
        import Inventario.signals
        print("✅ Signals de Inventario cargados correctamente")
