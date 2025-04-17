from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TodoForm, UpdateTodoForm
from .models import Todo


# Create your views here.
@login_required
def index(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'todos/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            print(f"Todo 저장: {todo.id}, {todo.get_priority_display()}")
            return redirect('todos:index')
    else:
        form = TodoForm()
    context = {
        'form': form,
    }
    return render(request, 'todos/create.html', context)


@login_required
def detail(request, pk):
    todo = Todo.objects.get(pk=pk)
    context = {
        'todo': todo,
    }
    return render(request, 'todos/detail.html', context)


@login_required
def update(request, pk):
    todo = Todo.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateTodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todos:detail', pk=pk)
    else:
        form = UpdateTodoForm(instance=todo)
    context = {
        'form': form,
        'todo': todo,
    }
    return render(request, 'todos/update.html', context)


@login_required
def delete(request, pk):
    todo = Todo.objects.get(pk=pk)
    if request.method == 'POST':
        todo.delete()
    return redirect('todos:index')
