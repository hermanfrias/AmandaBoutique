# Generated manually for adding proveedor and categoria fields to ExistenciaInsumo model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProveedoresApp', '0002_proveedores_rif'),
        ('Inventario', '0005_alter_existenciainsumo_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='existenciainsumo',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insumos', to='ProveedoresApp.proveedores'),
        ),
        migrations.AddField(
            model_name='existenciainsumo',
            name='categoria',
            field=models.CharField(choices=[('Telas', 'Telas'), ('Hilos', 'Hilos'), ('Adornos', 'Adornos'), ('Estructura', 'Estructura'), ('Otros', 'Otros')], default='Otros', max_length=20),
        ),
    ]
