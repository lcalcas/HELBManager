from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=True, unique=True)

    class Meta:
        pass

    def __str__(self):
        return f"{self.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="/")

    def __str__(self):
        return f"{self.user} (Profile)"

    def save(self, *args, **kwargs):
        super().save()
