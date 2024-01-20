from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #formulario de registro y autentificación
from django.contrib.auth.models import User # Modelo de usuario 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

# Registrar nuevo usuario
def signup(request):
    if request.method == 'GET':
        # Retorno el formulario de registro
        return render(request, 'signup.html',{
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']: # Comparar contraseñas
            try:
                # Registrar usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()# Guardar usuario
                login(request, user) # Crear la sesión del usuario (cookie)
                return redirect('tasks') # Redireccionar a la página de tareas
            except IntegrityError: # Manejo del error
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            'error': 'Password do not match'
        })
        
# Tareas (tareas pendientes - listar)
@login_required
def tasks(request):
    # Consulta para listar las tareas del usuario actual
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) 
    return render(request, 'tasks.html', {'tasks': tasks, 'title': 'Tasks pending', 'subtitle': 'No pending tasks'}) 
   
# Tareas (tareas completadas - listar)
@login_required
def completed_tasks(request):
    # Consulta para listar las tareas del usuario actual
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 
    return render(request, 'tasks.html', {'tasks': tasks, 'title': 'Tasks completed', 'subtitle': 'No tasks completed yet'})     

# Crear nueva tarea
@login_required
def create_task(request):
    if request.method == 'GET': 
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else: # Enviando datos ( crear tarea )
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user # Asignar usuario
            new_task.save() # Guardar en la BD
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor provee datos válidos'
            })

# Detalle de cada tarea
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user) # Consulta 
        form = TaskForm(instance=task) # Llenar el formulario con los datos de la tarea
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else: # Enviar datos ( Actualizar )
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user) # Consulta 
            form = TaskForm(request.POST, instance=task) # Actualizar
            form.save() # Guardar en la BD
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task,
                'form': form, 
                'error': 'Error updating task'
            })

# Tarea completada
@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
# Eliminar tarea
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def profile_user(request):
    return render(request, 'profile.html')    

# Cerrar sesión
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# Iniciar sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })     
    else:
        # Validar el usuario con la base de datos
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None: # Si el usuario está vacido
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            }) 
        else: # La validación es correcta
            login(request, user) # Crear la sesión del usuario
            return redirect('tasks') # Reedirecionar a la página de tareas
  
