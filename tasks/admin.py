from django.contrib import admin
from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'due_date', 'completed')
    list_filter = ('completed', 'category')
    search_fields = ('title',)
    list_select_related = ('category',)
