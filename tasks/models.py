from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
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
