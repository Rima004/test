from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django_filters import rest_framework as filters

from apps.tasks.filters import TasksFilter
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerialiser, TasksList


# Create your views here.

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

class Task_by_id(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialiser


