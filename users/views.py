from django.http import HttpResponse
from django.template import loader

from .forms import RegisterForm, LoginForm, PostForm
from .models import User, Post, Like
from django.contrib import  messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

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
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

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

def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'post_detail.html', {
        'post':post,
        'is_liked':is_liked,
    })

@login_required
def like_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    like, created = Like.objects.get_or_create(post=post, user= request.user)
    if not created:
        like.delete()
    return redirect('post_detail', post_pk=post.pk)