from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name='users'),
    path('users/details/<int:id>/', views.details, name='details'),
    path('register/', views.registration, name="register"),
    path('create/', views.create_post, name='create_post'),
    path('accounts/login/', views.login_view, name='login'),
    path('',views.show_posts, name='home'),
    path('post/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_pk>/like/', views.like_post_ajax, name='like_post_ajax'),
]