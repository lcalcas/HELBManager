# Generated by Django 4.1.3 on 2022-12-13 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0011_collaboration_is_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='collaborators',
        ),
        migrations.RemoveField(
            model_name='project',
            name='manager',
        ),
    ]
