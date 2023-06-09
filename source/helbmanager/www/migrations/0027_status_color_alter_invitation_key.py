# Generated by Django 4.1.3 on 2023-01-06 11:47

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0026_alter_changestatuslog_new_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='b4a073d906335996', max_length=16),
        ),
    ]
