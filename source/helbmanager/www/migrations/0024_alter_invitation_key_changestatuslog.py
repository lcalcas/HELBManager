# Generated by Django 4.1.3 on 2023-01-05 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0023_alter_invitation_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='df9855174ae9cfd3', max_length=16),
        ),
        migrations.CreateModel(
            name='ChangeStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='www.log')),
                ('new_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='csl_new_status', to='www.status')),
                ('old_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='csl_old_status', to='www.status')),
            ],
        ),
    ]