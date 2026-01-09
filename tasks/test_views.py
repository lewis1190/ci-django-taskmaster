from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Task, Category


class IndexViewTests(TestCase):
    """Skeleton tests for the `index` view in `tasks.views`.

    Each test is declared but intentionally not implemented yet. They
    use `self.skipTest("Not implemented")` so the test runner shows
    these as skipped placeholders.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('tasks:index')
        # create two categories and three tasks related to them
        self.work = Category.objects.create(name="Work")
        self.personal = Category.objects.create(name="Personal")
        now = timezone.now()
        self.task_report = Task.objects.create(
            title="Finish report",
            due_date=now + timedelta(days=1),
            completed=False,
            category=self.work,
        )
        self.task_email = Task.objects.create(
            title="Email client",
            due_date=now + timedelta(days=2),
            completed=False,
            category=self.work,
        )
        self.task_groceries = Task.objects.create(
            title="Buy groceries",
            due_date=now - timedelta(days=1),
            completed=True,
            category=self.personal,
        )

    def test_index_get_renders_template_and_context(self):
        """GET should render the index template with expected context."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertIn('tasks_uncompleted', response.context)
        self.assertIn('tasks_completed', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('task_form', response.context)

    def test_index_post_valid_creates_task_and_redirects(self):
        """POST with valid data should create a Task and redirect."""
        data = {
            'title': 'New Task',
            # `datetime-local` input expects `YYYY-MM-DDTHH:MM` (no timezone)
            'due_date': (timezone.now() + timedelta(days=3))
            .strftime('%Y-%m-%dT%H:%M'),
            # form expects the PK value for ModelChoiceField
            'category': self.work.pk,
        }
        response = self.client.post(reverse('tasks:index'), data)
        # successful POST should redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_index_post_invalid_shows_form_errors(self):
        """POST with invalid data should re-render form with errors."""
        data = {
            'title': '',  # missing title should be invalid
            'due_date': (timezone.now() + timedelta(days=3))
            .strftime('%Y-%m-%dT%H:%M'),
            'category': self.work.pk,
        }
        response = self.client.post(reverse('tasks:index'), data)
        self.assertEqual(response.status_code, 200)  # re-render form
        form = response.context['task_form']
        self.assertTrue(form.errors)
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])

    def test_tasks_lists_ordering_and_category_in_context(self):
        """Context should include `tasks_uncompleted`, `tasks_completed`, and
        `categories`."""
        response = self.client.get(self.url)
        tasks_uncompleted = response.context['tasks_uncompleted']
        tasks_completed = response.context['tasks_completed']
        categories = response.context['categories']

        # Check uncompleted tasks ordering
        self.assertEqual(len(tasks_uncompleted), 2)
        self.assertEqual(tasks_uncompleted[0], self.task_email)  # due later
        self.assertEqual(tasks_uncompleted[1], self.task_report)

        # Check completed tasks ordering
        self.assertEqual(len(tasks_completed), 1)
        self.assertEqual(tasks_completed[0], self.task_groceries)

        # Check categories in context
        self.assertIn(self.work, categories)
        self.assertIn(self.personal, categories)

    def test_index_uses_select_related_for_category(self):
        """Querysets should use `select_related('category')` for efficiency."""
        response = self.client.get(self.url)
        # evaluate the querysets so the main DB hit occurs here
        tasks_uncompleted = list(response.context['tasks_uncompleted'])
        tasks_completed = list(response.context['tasks_completed'])

        # accessing `category.name` should not issue additional queries
        with self.assertNumQueries(0):
            for task in tasks_uncompleted:
                _ = task.category.name
            for task in tasks_completed:
                _ = task.category.name

    def test_create_task_triggers_success_message_and_resets_form(self):
        """After successful POST, a success message is set and
        form is reset."""
        data = {
            'title': 'Another Task',
            'due_date': (timezone.now() + timedelta(days=4))
            .strftime('%Y-%m-%dT%H:%M'),
            'category': self.personal.pk,
        }
        response = self.client.post(reverse('tasks:index'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertTrue(any("Task added successfully." in str(m)
                        for m in messages))
        form = response.context['task_form']
        self.assertFalse(form.is_bound)  # form should be unbound (reset)
