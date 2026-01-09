from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import Manager
    # `Task` is defined below; use a forward-reference string in the annotation


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    if TYPE_CHECKING:
        tasks: "Manager[Task]"

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tasks',
    )

    class Meta:
        ordering = ['-due_date', 'title']

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.title
