from fileinput import FileInput
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from user.models import UserProfile



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email','password1', 'password2', )