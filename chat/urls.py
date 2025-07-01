from django.urls import path
from .views import add_contact, contact_list


urlpatterns = [
    path('contacts/add/', add_contact, name='add_contact'),
    path('contacts/', contact_list, name='contact_list'),
]