from django.db.transaction import commit
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.template.defaulttags import comment

from .forms import RegisterForm, LoginForm, PostForm, CommentForm, EditProfileForm
from .models import User, Post, Like, Tag, PostTag, Comment
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
    user_profile = User.objects.get(id=id)
    template = loader.get_template("details.html")
    context = {
        'user_profile': user_profile,
    }
    return  HttpResponse(template.render(context, request))

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account create')
            return  redirect('details')
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
                return redirect("details", id=user.id)

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

            raw_tags = request.POST.get('tags', '')
            tag_list = [t.strip().lower() for t in raw_tags.split(',') if t.strip()]
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                PostTag.objects.grt_or_creare(post=post, tag=tag)

            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def show_posts(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()


    comments = post.comments.all().order_by('-created_at')
    comment_form = CommentForm()


    if request.method == "POST" and 'comment_submit' in request.POST:
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', post_pk=post.pk)

    return render(request, 'post_detail.html', {
        'post':post,
        'is_liked':is_liked,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def like_post_ajax(request, post_pk):
    post = (get_object_or_404(Post, pk=post_pk))
    like, created = Like.objects.get_or_create(post=post, user= request.user)
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True
        print(like)
    return JsonResponse({
        "is_liked": is_liked,
        "likes_count": post.likes.count()
    })

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES,  instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('details', id=request.user.pk)
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})