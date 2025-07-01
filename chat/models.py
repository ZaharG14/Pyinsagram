from django.db import models
from django.conf import settings

class Massage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_massages')
    caption = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='received_messages')

class Contact(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"