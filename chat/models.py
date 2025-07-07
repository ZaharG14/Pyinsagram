from django.db import models
from django.conf import settings

from puinstagram.puinstagram.settings import AUTH_USER_MODEL


class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usernames = ', '.join(AUTH_USER_MODEL.username for user in self.participants.all())
        return f"Чат: {usernames}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='received_messages')
    caption = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} ➡ {self.receiver}: {self.caption}"

