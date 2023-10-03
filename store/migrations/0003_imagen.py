# Generated by Django 4.2.1 on 2023-07-27 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id_imagen', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='images/')),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('tipo_imagen', models.CharField(max_length=50)),
            ],
        ),
    ]
