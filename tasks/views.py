from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Task, Category
from .forms import TaskForm


def index(request):
    """
    Render an index page with separate lists for uncompleted
    and completed tasks.
    """
    categories = Category.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully.')
            # reset the form for a fresh blank form after successful save
            form = TaskForm()
            return redirect('tasks:index')
    else:
        form = TaskForm()

    # Fetch querysets once (after POST handling) so the page shows current data
    tasks_uncompleted = (
        Task.objects.select_related('category')
        .filter(completed=False)
        .order_by('-due_date', 'title')
    )
    tasks_completed = (
        Task.objects.select_related('category')
        .filter(completed=True)
        .order_by('-due_date', 'title')
    )

    return render(
        request,
        'tasks/index.html',
        {
            'tasks_uncompleted': tasks_uncompleted,
            'tasks_completed': tasks_completed,
            'categories': categories,
            'task_form': form,
        },
    )
