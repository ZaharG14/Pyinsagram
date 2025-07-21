from django.db import models
from django.conf import settings

class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following_set")
    subscribed_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers_set")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("subscriber", "subscribed_person")
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.subscriber.username} -> {self.subscribed_person.username}"