# Generated manually for model changes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0004_usoinsumo_detalleusoinsumo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='existenciainsumo',
            name='descripcion',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
