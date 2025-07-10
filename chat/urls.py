from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.chat_view, name='chat'),
    path('my/', views.chat_view, name='all_chats')
]