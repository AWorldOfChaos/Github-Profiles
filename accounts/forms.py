from django import forms
from django.contrib.auth.models import User
from accounts.models import Account
from django.contrib.auth.forms import UserCreationForm


# This Sign up form creates a custom sign-up
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = Account
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')
