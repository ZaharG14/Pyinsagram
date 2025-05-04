from django.contrib.auth.password_validation import password_changed
from django.forms import PasswordInput

from .models import User, Post
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.shortcuts import render


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, label='Input password')
    confirm_password = forms.CharField(max_length=65, widget=forms.PasswordInput, label='Check password')

    class Meta():
        model = User
        fields = ['username','phone']

    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords dont match")
        return clean_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label="Імя користувача", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')


        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Неправильне імя користувача або пароль")
        cleaned_data['user'] = user
        return cleaned_data

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]
        widgets = {
            'caption':forms.Textarea(attrs={'rows':3, 'placeholder':'Напишіть підпис...'}),
        }