from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "Les mots de passe ne correspondent pas !"
    }

    email = forms.EmailField(label="Courriel", label_suffix="")
    first_name = forms.CharField(label="Prénom", label_suffix="")
    last_name = forms.CharField(label="Nom de famille", label_suffix="")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="E-mail", label_suffix="")

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
