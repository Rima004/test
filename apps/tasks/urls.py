from django.urls import path

from apps.tasks.views import TaskCreate, ListTasks, Task_by_id, TaskUpdateStatus, TaskCompleted, AddComment, \
    ViewComments

urlpatterns = [
    path('new_task/',TaskCreate.as_view()),
    path('all_tasks/',ListTasks.as_view()),
    path('detail_task/<pk>',Task_by_id.as_view()),
    path('update_status_task/<pk>',TaskUpdateStatus.as_view()),
    path('completed_task/<pk>',TaskCompleted.as_view()),
    # path('remove_task/<int:task_id>',TaskRemove.as_view()),
    path('add_comment/',AddComment.as_view()),
    path('view_comments/<int:task_id>/',ViewComments.as_view())

]