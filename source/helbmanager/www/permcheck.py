from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Collaboration

User = get_user_model()


def is_user_in_project(user: User, project: Project):
    return Collaboration.objects.filter(user=user, project=project).count() == 1


def is_user_manager(user: User, project: Project):
    return Collaboration.objects.get(user=user, project=project).is_manager


def is_user_collaborator(user: User, project: Project):
    return is_user_in_project(user, project) and not is_user_manager(user, project)
