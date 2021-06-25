from django.contrib import admin
from .models import Event, TaskType, TakenEvent, TaskStatus

admin.site.register(Event)
admin.site.register(TaskType)
admin.site.register(TakenEvent)
admin.site.register(TaskStatus)

