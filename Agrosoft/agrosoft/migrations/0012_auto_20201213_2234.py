# Generated by Django 2.0.2 on 2020-12-14 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrosoft', '0011_auto_20201213_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='produ',
            field=models.IntegerField(null=True, verbose_name='Produccion'),
        ),
    ]
