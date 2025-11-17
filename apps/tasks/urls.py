from django.urls import path

from apps.tasks.views import TaskCreate, ListTasks, Task_by_id, TaskUpdateStatus, TaskCompleted, AddComment, \
    ViewComments, StartTimer, StopTimer

urlpatterns = [
    path('new_task/',TaskCreate.as_view(),name="new_task"),
    path('all_tasks/',ListTasks.as_view(),name="list_task"),
    path('detail_task/<pk>',Task_by_id.as_view(),name="detail_task"),
    path('update_status_task/<pk>',TaskUpdateStatus.as_view(),name='update_task'),
    path('completed_task/<pk>',TaskCompleted.as_view(),name='completed_task'),
    # path('remove_task/<int:task_id>',TaskRemove.as_view()),
    path('add_comment/',AddComment.as_view()),
    path('view_comments/<int:task_id>/',ViewComments.as_view()),
    path("log_task/",StartTimer.as_view()),
    path("stop_timer/",StopTimer.as_view())

]