from random import choices

from django_filters import rest_framework as filters

from apps.tasks.models import Task


class TasksFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name='user_id',lookup_expr='exact')
    status = filters.ChoiceFilter(choices=Task.STATUS)

    class Meta:
        model=Task
        fields=['user_id']
