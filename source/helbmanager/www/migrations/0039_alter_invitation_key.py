# Generated by Django 4.1.3 on 2023-01-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0038_alter_invitation_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='10d7846cfac557bb', max_length=16),
        ),
    ]
