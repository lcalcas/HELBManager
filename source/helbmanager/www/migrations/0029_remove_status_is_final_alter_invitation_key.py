# Generated by Django 4.1.3 on 2023-01-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0028_alter_invitation_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='is_final',
        ),
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='71559d9e4df281b4', max_length=16),
        ),
    ]
