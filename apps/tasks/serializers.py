
from rest_framework import serializers

from apps.tasks.models import Task


class TaskSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields = ['id','title', 'description', "status",'user']
        read_only_fields=['status','user','id']


class TasksList(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['id','title']