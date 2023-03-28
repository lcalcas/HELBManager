from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import *

User = get_user_model()


def get_collaborations(**kwargs):
    if 'project' in kwargs:
        project = kwargs['project']
        if 'is_manager' in kwargs:
            is_manager = kwargs['is_manager']
            return list(Collaboration.objects.filter(project=project, is_manager=is_manager))
        return list(Collaboration.objects.filter(project=project))
    elif 'user' in kwargs:
        user = kwargs['user']
        return list(Collaboration.objects.filter(user=user))
    else:
        return list()


def get_collaborators(project: Project):
    return [col.user for col in get_collaborations(project=project, is_manager=False)]


def get_manager(project: Project):
    return get_collaborations(project=project, is_manager=True)[0].user


def get_team(project: Project):
    return [col.user for col in get_collaborations(project=project)]


def get_active_tasks(**kwargs):
    if 'project' and 'user' in kwargs:
        return Task.objects.filter(project=kwargs['project'], user=kwargs['user'], is_active=True)
    elif 'project' in kwargs:
        return Task.objects.filter(project=kwargs['project'], is_active=True)
    elif 'user' in kwargs:
        return Task.objects.filter(user=kwargs['user'], is_active=True)
    elif 'all' in kwargs:
        return Task.objects.filter(is_active=kwargs['all'])


def get_projects(**kwargs):
    if 'user' in kwargs:
        return [col.project for col in get_collaborations(user=kwargs['user'])]
    else:
        return list()


def update_manager(**kwargs):
    if 'project' and 'new_manager' in kwargs:
        project = kwargs['project']
        new_manager = kwargs['new_manager']
        collaborations = get_collaborations(project=project, is_manager=True)
        collaborations += get_collaborations(project=project, user=new_manager)
        for col in collaborations:
            col.is_manager = not col.is_manager
            col.save()


def remove_collaborator(user: User, project: Project) -> None:
    collaboration = Collaboration.objects.get(user=user, project=project)
    collaboration.delete()


def get_status(post):
    result = []
    for key in post:
        if key.startswith("new-status"):
            result.append(post.get(key)[0])
        return result


def is_project_set_up(project):
    return Status.objects.filter(project=project, is_final=True).count() == 1


def gen_log_info(**kwargs):
    result = ""
    if kwargs['type']:
        type = kwargs.get('type')
        task_title = kwargs.get('task_title')
        author = kwargs.get('author')
        match type:
            case 'update':
                old = kwargs.get('old_st')
                new = kwargs.get('new_st')
                result += "Mise à jour statut:"
                result += f"\n\t- Ancien statut: {old}"
                result += f"\n\t- Nouveau statut: {new}"
            case 'new':
                result += "Ajout tâche"
            case 'delete':
                result += "Suppression tâche"
            case _:
                result = ""
    return result