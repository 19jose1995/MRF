# Generated by Django 5.2.3 on 2025-06-18 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0004_cargoprovincial_provincia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
                ('sector', models.CharField(max_length=100)),
                ('colegio', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('oficio', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
