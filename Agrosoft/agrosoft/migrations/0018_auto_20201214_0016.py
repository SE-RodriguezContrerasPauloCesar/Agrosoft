# Generated by Django 2.0.2 on 2020-12-14 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agrosoft', '0017_auto_20201214_0015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventmember',
            old_name='user',
            new_name='lote',
        ),
        migrations.AlterUniqueTogether(
            name='eventmember',
            unique_together={('event', 'lote')},
        ),
    ]