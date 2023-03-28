import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from .forms import *
from .models import *
from .permcheck import *
from .shortcuts import *

User = get_user_model()

@login_required
def index(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        context['projects_managers'] = [(pro, get_collaborations(project=pro, is_manager=True)[0].user) for pro in
                                        get_projects(user=user)]
        context['notifications'] = Notification.objects.filter(user=user, has_seen=False)
        print(context['notifications'])
        if request.method == 'POST':
            create_form = ProjectCreationForm(request.POST)
            join_form = ProjectJoinForm(request.POST)

            if create_form.is_valid():
                new_project = create_form.save()

                if new_project.id:
                    Collaboration.objects.create(project=new_project, user=user, is_manager=True)
                    return redirect('project-detail', pk=new_project.id)
                return redirect('index')

            if join_form.is_valid():
                presumed_invitation = Invitation.objects.filter(key=request.POST['key'], is_active=True)
                print(presumed_invitation)
                if presumed_invitation.count() == 1:
                    invitation = presumed_invitation[0]
                    if invitation.id:
                        project_to_join = invitation.project
                        if project_to_join.id:
                            if not is_user_in_project(user, project_to_join):
                                Collaboration.objects.create(user=request.user, project=project_to_join, is_manager=False)
                                invitation.receivers.add(user)
                                invitation.save()
                                return redirect('project-detail', pk=project_to_join.id)
                            else:
                                messages.error(request, "Vous faites déjà partie du projet")
                        else:
                            messages.error(request, "Pas de projet correspondant")
                    else:
                        messages.error(request, "Clé invalide")

            if 'notification-id' in request.POST:
                notification = Notification.objects.get(id=request.POST['notification-id'])
                notification.has_seen = True
                notification.save()

                return redirect('index')
        else:
            create_form = ProjectCreationForm()
            join_form = ProjectJoinForm()

        context['create_form'] = create_form
        context['join_form'] = join_form
    return render(request, 'www/index.html', context)


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, id=pk)
    user = request.user

    if is_user_in_project(request.user, project):
        collaborators = get_collaborators(project=project)
        is_manager = is_user_manager(request.user, project)
        tasks = get_active_tasks(project=project)
        context = {
            'project': project,
            'init_on_load': True,
            'manager': get_manager(project),
            'is_manager': is_manager,
            'collaborators': collaborators,
            'tasks': tasks,
            'status': Status.objects.filter(project=project),
            'team': get_team(project=project),
        }

        if is_manager:
            invitations = Invitation.objects.filter(project=project, is_active=True)
            if invitations.count() == 1:
                context['invitation_key'] = Invitation.objects.get(project=project, is_active=True)
            else:
                context['invitation_key'] = None

        task_form = TaskCreationForm()

        if request.method == 'POST':
            data = request.POST
            if 'new-task' in data:
                if is_manager:
                    task_form = TaskCreationForm(data)
                    if task_form.is_valid():
                        new_task = task_form.save(commit=False)
                        new_task.project = project
                        new_task.user = None
                        new_task.save()
                        if new_task.id:
                            TaskState.objects.create(task=new_task, user=user)
                            Log.objects.create(type='add', task=new_task)
                return redirect('project-detail', pk=pk)
            else:
                task = get_object_or_404(Task, id=data['task-id'], is_active=True)
                if 'delete-task' in data and is_manager:
                    task.get_last_task_state().close()
                    task.is_active = False
                    task.save()
                    Log.objects.create(type='rem', task=task)
                elif 'update-task' in data:
                    if user == task.user or is_manager:
                        new_sts = None
                        if data.get('task-st-id'):
                            new_sts = Status.objects.get(id=data['task-st-id']) if int(data['task-st-id']) > 0 else None
                        if task.status != new_sts:
                            try:
                                task.get_last_task_state().close()
                            except:
                                pass
                            TaskState.objects.create(task=task, user=request.user, status=new_sts)
                            Log.objects.create(type='upd', task=task)
                        task.status = new_sts

                        if is_manager and data['designation']:
                            new_des = data['designation']
                            task.designation = new_des
                    if is_manager:
                        if int(data['user-id']) > 0:
                            new_task_user = User.objects.get(id=data['user-id'])
                            task.user = new_task_user if is_user_in_project(new_task_user, project) else None
                        else:
                            task.user = None

                    task.save()

                    return redirect('project-detail', pk=pk)

            """if request.method == 'POST':
                data = request.POST
                task_form = TaskCreationForm(data)
                if data.get('designation'):
                    new_task = task_form.save(commit=False)
                    new_task.user = request.user
                    new_task.project = project
                    new_task.save()
            else:
                context['t_form'] = TaskCreationForm()"""
        context['t_form'] = task_form
        return render(request, 'www/project_detail.html', context)
    else:
        return redirect('index')


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, id=pk, is_active=True)

    if is_user_manager(request.user, project):
        context = {}
        context['id'] = pk
        context['project'] = project
        context['collaborators'] = collaborators = get_collaborators(project=project)
        context['form'] = ProjectUpdateForm(collaborators=collaborators, instance=project)
        context['status'] = Status.objects.filter(project=project)

        # Redirection après envoi form
        if request.method == 'POST':
            data = request.POST
            print(data)
            # Actualisation informations générales
            if 'info-update' in data:
                context['form'] = ProjectUpdateForm(collaborators=collaborators, data=data, instance=project)

                # Nouveau titre
                new_title = data['title']
                if new_title:
                    project.title = new_title
                else:
                    messages.error(request, "Le nouveau titre ne peut être une chaîne vide.")

                # Nouveau chef de projet
                new_manager_id = data['manager_id']
                if new_manager_id:
                    new_manager = User.objects.get(id=new_manager_id)
                    if is_user_collaborator(new_manager, project):
                        # before 3.1 - project.collaborators.add(project.manager)
                        # after 3.1 -

                        update_manager(new_manager=new_manager, project=project)

                        # before 3.1 - project.manager = new_manager
                        #   project.collaborators.remove(new_manager)

                project.description = data['description']
                project.save()

            elif 'collaborator-remove' in data:
                if data['user-id']:
                    user_to_rem = User.objects.get(id=data['user-id'])
                    if is_user_collaborator(user_to_rem, project):
                        remove_collaborator(user=user_to_rem, project=project)
                    else:
                        messages.error(request, "Une erreur est survenue.")
                else:
                    messages.error(request, "Une erreur est survenue.")

            elif 'append-status' in data:
                designation = data.get('designation')
                color = data.get('color')
                Status.objects.create(designation=designation, project=project, color=color)

            elif 'update-status' in data:
                status_id = data.get('update-status')
                designation = data.get('designation')
                color = data.get('color')
                status = get_object_or_404(Status, id=status_id)
                if 'delete-status' in data:
                    status.delete()
                else:
                    status.designation = designation
                    status.color = color
                    status.save()
        else:
            return render(request, 'www/project_update.html', context)
    return redirect('project-detail', pk=project.id)


@login_required
def generate_new_key(request, pk):
    project = get_object_or_404(Project, id=pk, is_active=True)

    if is_user_manager(request.user, project):
        keys = Invitation.objects.filter(project=project, is_active=True)
        for k in keys:
            k.is_active = False
            k.save()

        Invitation.objects.create(key=secrets.token_hex(8), project=project, is_active=True, creator=request.user)

    return redirect('project-detail', pk=project.id)


@login_required
def timeline(request, pk):
    user = request.user
    project = get_object_or_404(Project, id=pk, is_active=True)
    is_manager = is_user_manager(user, project)
    team = get_team(project)

    context = {
        'project': project,
        'is_manager': is_manager,
        'team': team
    }

    if is_manager:
        tasks = get_active_tasks(project=project)

        context['tasks'] = tasks
        context['status'] = Status.objects.filter(project=project)

        for s in context['status']:
            print(s.get_task_states())

        date_diff_btw_creation = datetime.datetime.now(datetime.timezone.utc) - project.datetime_created
        context['unit'] = "day" if (date_diff_btw_creation.seconds // 3600) > 24 else "hour"

        if request.method == 'POST':
            data = request.POST
            print(data)
            if 'analysis-user-id' in data:
                if data.get('analysis-user-id') != "0":
                    analysis_user = get_object_or_404(User, id=data.get('analysis-user-id'))
                    context['analysis_user'] = analysis_user

                    analysis_user_tasks = get_active_tasks(project=project, user=analysis_user)
                    analysis_user_data = {}
                    for t in analysis_user_tasks:
                        status_designation = "Sans status"
                        color = "#ffffff"
                        if t.status:
                            status_designation = t.status.designation
                            color = t.status.color
                        if status_designation not in analysis_user_data:
                            analysis_user_data[status_designation] = {
                                'nb': 0
                            }
                        analysis_user_data[status_designation]['nb'] += 1
                        analysis_user_data[status_designation]['color'] = color
                    context['analysis_user_data'] = analysis_user_data
                else:
                    context['analysis_user'] = None
        return render(request, 'www/project_timeline.html', context=context)
    return redirect('project-detail', pk=pk)


"""
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'manager']
    template_name_suffix = "_update"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
"""
