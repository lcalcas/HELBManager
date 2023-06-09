# Generated by Django 4.1.3 on 2023-01-05 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0025_alter_invitation_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changestatuslog',
            name='new_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='csl_new_status', to='www.status'),
        ),
        migrations.AlterField(
            model_name='changestatuslog',
            name='old_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='csl_old_status', to='www.status'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='ff32ce9894bc99d8', max_length=16),
        ),
    ]
