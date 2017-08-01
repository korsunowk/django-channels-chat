from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    recipients = models.ManyToManyField(User)


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages')
    sender = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    text = models.CharField(max_length=255, null=False, blank=False, default=None)
