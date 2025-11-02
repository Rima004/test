from django.conf import settings
from django.dispatch import receiver
from django.utils.timezone import override
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from django.db.models.signals import post_save
from apps.tasks.filters import TasksFilter
from apps.tasks.models import Task, Comment
from apps.tasks.serializers import TaskSerialiser, TasksList, TaskUpdateStatusSerialiser, CommetsSerialiser
from django.core.mail import send_mail

# Create your views here.

@receiver(post_save,sender=Task)
def send_email(sender, instance, created, **kwargs):
        if created:
            new_task = instance.user.email
            send_mail("New task for you", "Hi", settings.EMAIL_HOST_USER, [new_task])
        else:
            if(instance.status == 'Completed'):
                send_mail("The task completed",f"Title task: {instance.title}",settings.EMAIL_HOST_USER, [instance.user.email])


@receiver(post_save,sender=Comment)
def new_comment(sender, instance, created, **kwargs):
    if created:
        owner = instance.task_id.user.email
        send_mail("New comment for you", "Hi", settings.EMAIL_HOST_USER, [owner])



class TaskCreate(CreateAPIView):
    serializer_class=TaskSerialiser
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
       serializer = self.serializer_class(data=request.data)
       serializer.is_valid(raise_exception=True)

       new_task = serializer.save(user=request.user)

       return Response({'title': new_task.title,
                        'description':new_task.description,
                        'status': new_task.status,
                        'user': new_task.user.id
                        },status=HTTP_200_OK)




class ListTasks(ListAPIView):
    serializer_class = TasksList
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TasksFilter
    queryset = Task.objects.all()

class Task_by_id(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialiser


class TaskUpdateStatus(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateStatusSerialiser
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class TaskCompleted(APIView):

    def post (self, request, pk):
        updated_task = Task.objects.filter(pk=pk).update(status='Completed')
        if updated_task == 0:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"completed": "yes"}, status=status.HTTP_200_OK)

# class TaskRemove(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def delete(self,request,task_id):
#         deleted =Task.odjects.filter(id=task_id).delete()
#         if deleted == 0:
#             return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
#         return Response({"removed": "yes"}, status=status.HTTP_200_OK)


class AddComment(APIView):
  permission_classes = [IsAuthenticated]
  serializer_class = CommetsSerialiser

  def post(self,request):
      serializer = self.serializer_class(data=request.data)
      serializer.is_valid(raise_exception=True)
      new_comment = serializer.save()
      return Response({'comment': new_comment.id})



class ViewComments(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_field = 'task_id'
    serializer_class = CommetsSerialiser




