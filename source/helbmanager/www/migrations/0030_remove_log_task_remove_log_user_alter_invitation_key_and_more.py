# Generated by Django 4.1.3 on 2023-01-07 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0029_remove_status_is_final_alter_invitation_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='task',
        ),
        migrations.RemoveField(
            model_name='log',
            name='user',
        ),
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='7dd622cd652c77f4', max_length=16),
        ),
        migrations.DeleteModel(
            name='ChangeStatusLog',
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
