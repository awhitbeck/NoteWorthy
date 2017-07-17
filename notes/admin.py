from django.contrib import admin

from .models import *

admin.site.register(Project)
admin.site.register(Note)
admin.site.register(ToDoTask)
# admin.site.register(ToDoList)

# Register your models here.
