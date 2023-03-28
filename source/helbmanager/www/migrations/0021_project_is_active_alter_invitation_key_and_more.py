# Generated by Django 4.1.3 on 2023-01-03 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0020_task_is_active_alter_invitation_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='f952122310bf5c26', max_length=16),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='www.task')),
            ],
        ),
    ]