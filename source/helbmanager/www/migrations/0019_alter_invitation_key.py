# Generated by Django 4.1.3 on 2022-12-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0018_alter_collaboration_is_manager_alter_invitation_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='7852a4fa581b85b9', max_length=16),
        ),
    ]
