from django.shortcuts import render

from .models import Task, Category


def index(request):
    """
    Render an index page with separate lists for uncompleted
    and completed tasks.
    """
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
    categories = Category.objects.all()
    return render(
        request,
        'tasks/index.html',
        {
            'tasks_uncompleted': tasks_uncompleted,
            'tasks_completed': tasks_completed,
            'categories': categories,
        },
    )
