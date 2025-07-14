from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('all_chats/', views.all_chats_view, name='all_chats')
]