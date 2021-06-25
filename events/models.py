from django.contrib.sessions.backends import file
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class TaskType(models.Model):
    name = models.CharField(max_length=30, help_text="Enter a task type ")

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    name = models.CharField(max_length=30, help_text="Enter a task status ")

    def __str__(self):
        return self.name


class Event(models.Model):
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=256)
    descriptions = models.CharField(max_length=512)
    event_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(TaskStatus, default=1, on_delete=models.CASCADE, null=True)
    data_limit = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (("create_event", "Able to create new event"),)


class TakenEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    performer = models.ForeignKey(User, related_name='performer', on_delete=models.CASCADE, null=True)
    AcceptanceTime = models.DateTimeField(default=datetime.now, blank=True)
    response_file = models.FileField(upload_to='user/requests/', null=True, blank=True, default=None)
