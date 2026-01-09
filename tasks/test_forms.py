from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .forms import TaskForm
from .models import Category, Task


class TaskFormTests(TestCase):
    """Skeleton tests for `TaskForm`.

    Each test is declared but intentionally not implemented so you can
    iterate through them interactively.
    """

    def setUp(self):
        self.category = Category.objects.create(name="Work")
        self.now = timezone.now()

    def test_form_valid_with_proper_data(self):
        """Form should validate when given a title, category PK, and proper
        due_date."""
        data = {
            'title': 'Test Task',
            'due_date': (self.now + timedelta(days=1))
            .strftime('%Y-%m-%dT%H:%M'),
            'category': self.category.pk,
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_title(self):
        """Form should be invalid if the title is missing."""
        data = {
            'title': '',
            'due_date': (self.now + timedelta(days=1))
            .strftime('%Y-%m-%dT%H:%M'),
            'category': self.category.pk,
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_invalid_bad_due_date_format(self):
        """Form should reject improperly formatted `due_date` values."""
        data = {
            'title': 'Test Task',
            'due_date': 'invalid-date-format',
            'category': self.category.pk,
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_form_requires_category(self):
        """Form should require a category selection."""
        data = {
            'title': 'Test Task',
            'due_date': (self.now + timedelta(days=1))
            .strftime('%Y-%m-%dT%H:%M'),
            'category': '',
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_form_saves_creates_task(self):
        """Calling `form.save()` should create a `Task` instance with
        provided data."""
        data = {
            'title': 'Test Task',
            'due_date': (self.now + timedelta(days=1))
            .strftime('%Y-%m-%dT%H:%M'),
            'category': self.category.pk,
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, data['title'])
        self.assertEqual(task.category, self.category)
