# Generated by Django 4.1.3 on 2022-12-03 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_bio_alter_profile_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]