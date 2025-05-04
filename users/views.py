from lib2to3.fixes.fix_input import context

from django.contrib.auth.password_validation import password_changed
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import RegisterForm, LoginForm, PostForm
from .models import User
from django.contrib import  messages

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post

def users(request):
    myusers = User.objects.all().values()
    template = loader.get_template('all_users.html')
    context = {
        'myusers': myusers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myuser = User.objects.get(id=id)
    template = loader.get_template("details.html")
    context = {
        'myuser': myuser,
    }
    return  HttpResponse(template.render(context, request))

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account create')
            return  redirect('users')
        else:
            messages.error(request, 'Edit your on the form')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]
            user = authenticate(request, phone=phone, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

def show_posts(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'show_posts.html', {'posts': posts})