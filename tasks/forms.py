from django import forms
from .models import Task

# Formulario para crear tareas
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task # Tabla
        fields = ['title', 'description', 'important'] # Campos del formulario
        widgets = { # Estilizar el formulario (campos)
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description', 'rows': '3'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }