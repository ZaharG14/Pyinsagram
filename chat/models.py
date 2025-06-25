from django.db import models
from django.conf import settings

class Massage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_massages')
    caption = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='received_messages')