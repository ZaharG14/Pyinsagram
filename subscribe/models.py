from django.db import models
from django.conf import settings

class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following_set")
    subscribed_person = models.ForeignKey(settings.AUTH_USER_MODEL)
