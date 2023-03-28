from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(Status)
admin.site.register(Collaboration)
admin.site.register(Task)
admin.site.register(Invitation)
admin.site.register(TaskState)
admin.site.register(Log)
admin.site.register(Notification)
# 2.2 -- modification tables
# admin.site.register(UserProject)