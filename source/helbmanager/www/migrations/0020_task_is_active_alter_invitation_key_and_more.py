# Generated by Django 4.1.3 on 2023-01-03 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('www', '0019_alter_invitation_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_active',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='a6558ddbf49459fa', max_length=16),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='t_status', to='www.status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='t_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
