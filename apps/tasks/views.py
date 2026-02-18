from django.conf import settings
from django.utils.timezone import now
from django.dispatch import receiver
from django.utils.timezone import override
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from django.db.models.signals import post_save
from yaml import serialize

from apps.tasks.filters import TasksFilter
from apps.tasks.models import *
from apps.tasks.serializers import TaskSerialiser, TasksList, TaskUpdateStatusSerialiser, CommetsSerialiser, \
    TimerSerializer
from django.core.mail import send_mail
from apps.tasks.tasks import *
# Create your views here.




class TaskCreate(CreateAPIView):
    serializer_class=TaskSerialiser
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
       serializer = self.serializer_class(data=request.data)
       serializer.is_valid(raise_exception=True)

       new_task = serializer.save(user=request.user)
       send_email.delay('New task for you',new_task.user.email)
       return Response({'title': new_task.title,
                        'description':new_task.description,
                        'status': new_task.status,
                        'user': new_task.user.id
                        },status=HTTP_201_CREATED)




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
        updated_task=get_object_or_404(queryset=Task.objects.all(),pk=pk)
        updated_task.status='Completed'
        updated_task.save()
        completed_task.delay("Your task is completed", updated_task.user.email)
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
      new_comment.delay("Hi,new comment",new_comment.user.email)
      return Response({'comment': new_comment.id})



class ViewComments(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_field = 'task_id'
    serializer_class = CommetsSerialiser


class StartTimer(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class =TimerSerializer
    def post(self,request):
        task = Task.objects.get(id=request.data["task"])
        user = task.user



        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"timer":"start"})


class  StopTimer(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimerSerializer

    def post(self,request):
        task=Task.objects.get(id=request.data['task'])
        timer=Timer.objects.get(task=task)
        timer.stop =now()
        timer.duration = now()-timer.start
        timer.save()
        return Response({"message":"timer is stop",
                         "duraton":timer.duration})



