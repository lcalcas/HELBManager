import datetime
import secrets
import uuid
import random
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from colorfield.fields import ColorField

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=45, default="title")
    description = models.TextField(max_length=512, default="/")
    datetime_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return f"{self.title}"

    def get_team(self):
        return [collaboration.user for collaboration in Collaboration.objects.filter(project=self)]

    def get_tasks(self, active=True):
        return Task.objects.filter(project=self, is_active=active)

    def get_status(self):
        return Status.objects.filter(project=self)


class Collaboration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project")
    is_manager = models.BooleanField(default=False)
    datetime_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project} <-> {self.user}" + (" -MANAGER" if self.is_manager else "")


class Status(models.Model):
    designation = models.CharField(max_length=45, default="Statut")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_set")
    color = ColorField(default="#FFFFFF")

    class Meta:
        verbose_name_plural = "Status"

    def __str__(self):
        return f"{self.designation}"

    def get_task_states(self):
        return TaskState.objects.filter(status=self, task__in=Task.objects.filter(is_active=True))

    def get_tasks(self, active=True):
        return Task.objects.filter(status=self, is_active=active)

    def get_ratio(self, active_tasks=True):
        project_tasks_count = self.project.get_tasks().count()
        self_tasks_count = Task.objects.filter(status=self, is_active=active_tasks).count()
        return self_tasks_count * 100 / project_tasks_count


class Task(models.Model):
    designation = models.CharField(max_length=45, default="Tâche")
    is_active = models.BooleanField(default=1)
    subtask_id = models.IntegerField(default=0)
    datetime_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="t_user")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="t_project")
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="t_status")

    def __str__(self):
        return f"{self.designation}"

    def get_last_task_state(self):
        return TaskState.objects.get(task=self, datetime_stop=None)


class Invitation(models.Model):
    key = models.CharField(max_length=16, default=secrets.token_hex(8))
    datetime_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="i_project")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="i_creator")
    receivers = models.ManyToManyField(User, blank=True, related_name="i_receivers")

    def __str__(self):
        return f"{self.project} - by {self.creator} the {self.datetime_created.strftime('%Y-%m-%d')}"


class TaskState(models.Model):
    datetime_start = models.DateTimeField(auto_now_add=True)
    datetime_stop = models.DateTimeField(blank=True, null=True, default=None)

    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.datetime_start.strftime('%Y-%m-%d %H:%M:%S')} by {self.user} on {self.task}"

    def close(self):
        self.datetime_stop = timezone.now()
        self.save()


class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=49)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in self.task.project.get_team():
            if self.type == 'add':
                text = "Nouvelle tâche : "
                text += f"\n'{self.task}'"
            elif self.type == 'rem':
                text = "Suppression tâche : "
                text += f"\n'{self.task}'"
            elif self.type == 'upd':
                text = "Mise à jour statut : "
                text += f"\n{self.task}: {self.task.status}"
            Notification.objects.create(user=user, log=self, text=text)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    has_seen = models.BooleanField(default=False)
    text = models.TextField()
