# Generated by Django 4.2.1 on 2023-09-27 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_pedido'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='pedido',
            table='store_pedido',
        ),
    ]