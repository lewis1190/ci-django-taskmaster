from django import forms

from .models import Task, Category


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter task title',
                   'class': 'form-control', 'required': True}
        ),
        label='Title',
    )

    due_date = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control',
                   'required': True}
        ),
        label='Due date',
    )
    # `category` is required by the model (ForeignKey without null=True),
    # declare it explicitly to ensure ordered choices and required behavior.
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('name'),
        required=True,
        label='Category',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select', 'required': True}),
    )

    class Meta:
        model = Task
        fields = ['title', 'category', 'due_date']

    # Note: no explicit __init__ required — default ModelForm behavior is
    # sufficient.
