from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", ) # Campo de solo lectura

# Registrar el modelo tareas en el panel admin
admin.site.register(Task, TaskAdmin) 

