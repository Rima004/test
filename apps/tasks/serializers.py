
from rest_framework import serializers

from apps.tasks.models import Task, Comment, Timer
from apps.users.models import User


class TaskSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields = ['id','title', 'description', "status",'user']
        read_only_fields=['status','user','id']


class TasksList(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['id','title']


class TaskUpdateStatusSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['id','status']



class CommetsSerialiser(serializers.ModelSerializer):
    task_id=serializers.PrimaryKeyRelatedField (queryset=Task.objects.all(), write_only=True)
    class Meta:
        model=Comment
        fields=['text','task_id']

class TimerSerializer(serializers.ModelSerializer):

   task=serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

   class Meta:
       model=Timer
       fields=['start','task',"user","stop","duration"]
       read_only_fields=['user','stop','start','duration']




