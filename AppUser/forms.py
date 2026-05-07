from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'college_name', 'skills']