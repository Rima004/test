from django.urls import path

from apps.tasks.views import TaskCreate, ListTasks, Task_by_id

urlpatterns = [
    path('new_task/',TaskCreate.as_view()),
    path('all_tasks/',ListTasks.as_view()),
    path('detail_task/<pk>',Task_by_id.as_view()),

]