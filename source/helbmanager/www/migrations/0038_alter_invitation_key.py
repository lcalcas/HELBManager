# Generated by Django 4.1.3 on 2023-01-08 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0037_notification_text_alter_invitation_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(default='18717f480dc88f38', max_length=16),
        ),
    ]