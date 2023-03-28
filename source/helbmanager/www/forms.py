from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .shortcuts import *

User = get_user_model()


class ProjectCreationForm(forms.ModelForm):
    title = forms.CharField(label="Titre", label_suffix="")
    description = forms.CharField(label="Description", label_suffix="")

    class Meta:
        model = Project
        fields = ['title', 'description']


class ProjectUpdateForm(forms.ModelForm):
    manager_id = forms.ChoiceField(required=False, label="Chef de projet", label_suffix="")

    class Meta:
        model = Project
        fields = ['title', 'manager_id', 'description']

    def __init__(self, collaborators, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        selection = [(col.id, col.username) for col in collaborators]
        self.fields['manager_id'].choices = ([(None, "-------")] + selection)


class ProjectJoinForm(forms.Form):
    key = forms.CharField(max_length=16, label="Clé", label_suffix="")


class TaskCreationForm(forms.ModelForm):
    designation = forms.CharField(label="")

    class Meta:
        model = Task
        fields = ['designation']


class TaskUpdateForm(forms.ModelForm):
    designation = forms.CharField(label="", label_suffix="")
    teammember_id = forms.ChoiceField(required=True, label="", label_suffix="")

    class Meta:
        model = Task
        fields = ['designation', 'teammember_id']

    def __init__(self, t_id, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        task = Task.objects.get(id=t_id)
        project = task.project
        user = task.user
        selection = get_team(project=project)
        selection.remove(user)
        self.fields['teammember_id'].choices = ([(user.id, user.username)] + [(s.id, s.username) for s in selection])
