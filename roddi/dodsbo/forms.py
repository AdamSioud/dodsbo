from django import forms
from .models import Dodsbo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


class AddMemberToDodsboForm(forms.ModelForm):
    class Meta:
        model = Dodsbo
        fields = ["id"]
