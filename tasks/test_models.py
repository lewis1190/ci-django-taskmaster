from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from tasks.models import Category, Task


class TaskModelTest(TestCase):
    """Test skeleton for the Task model."""

    def setUp(self):
        # create a category and a couple of tasks for use in tests
        self.category = Category.objects.create(name="Test Category")
        now = timezone.now()
        self.task_future = Task.objects.create(
            title="Future Task",
            due_date=now + timedelta(days=1),
            completed=False,
            category=self.category,
        )
        self.task_past = Task.objects.create(
            title="Past Task",
            due_date=now - timedelta(days=1),
            completed=True,
            category=self.category,
        )

    def test_str_returns_title(self):
        """The Task.__str__ should return the task title."""
        self.assertEqual(str(self.task_future), "Future Task")
        self.assertEqual(str(self.task_past), "Past Task")

    def test_default_completed_is_false(self):
        """New tasks should default `completed` to False."""
        new_task = Task.objects.create(
            title="New Task",
            due_date=timezone.now() + timedelta(days=2),
            category=self.category,
        )
        self.assertFalse(new_task.completed)

    def test_ordering_by_due_date(self):
        """Tasks should be ordered by `-due_date`, then `title`
        per Meta.ordering."""
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], self.task_future)
        self.assertEqual(tasks[1], self.task_past)

    def test_category_relationship(self):
        """Category should have a reverse relation `tasks` to Task objects."""
        tasks_in_category = self.category.tasks.all()
        self.assertIn(self.task_future, tasks_in_category)
        self.assertIn(self.task_past, tasks_in_category)

    def test_create_task(self):
        """Creating a Task should persist provided fields and relations."""
        self.assertEqual(self.task_future.title, "Future Task")
        self.assertFalse(self.task_future.completed)
        self.assertEqual(self.task_future.category, self.category)
        self.assertIsNotNone(self.task_future.due_date)

    # Generate a unit test that checks for an error if the title is longer
    # than 100 characters
    def test_title_max_length(self):
        """Creating a Task with a title longer than 100 characters
        should raise a ValidationError."""
        from django.core.exceptions import ValidationError

        long_title = "A" * 101  # 101 characters
        task = Task(
            title=long_title,
            due_date=timezone.now() + timedelta(days=1),
            completed=False,
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            task.full_clean()  # This will trigger the validation
