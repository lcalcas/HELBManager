from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .functions import create_username
from .models import User, Profile


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if instance.id is None:
        instance.username = create_username(instance.first_name, instance.last_name)


@receiver(post_save, sender=User)
def user_creation(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)


"""
@receiver(post_save, sender=User)
def user_modification(sender, instance, **kwargs):
    instance.profile.save()
"""