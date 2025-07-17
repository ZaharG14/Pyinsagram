from django.urls import path
from . import views
from .views import follow_toggle

urlpatterns = [
    path('toggle/<str:username>/', follow_toggle, name='toggle')
]