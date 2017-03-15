from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.Form):

    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        # Checks if password is repeated in form
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise ValidationError('Password fields must match')
        return self.cleaned_data

    def clean_username(self):
        # Checks if username exists
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean_email(self):
        # Checks if email exists
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email
