# Generated manually for adding rif field to Proveedores model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProveedoresApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedores',
            name='rif',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
