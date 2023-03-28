# Generated by Django 4.1.3 on 2023-01-07 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('www', '0035_remove_project_progression_alter_invitation_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=49)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='www.task')),
            ],
        ),
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='2a8d7282c85e1cdb', max_length=16),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_seen', models.BooleanField(default=False)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='www.log')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]