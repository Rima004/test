
from rest_framework import serializers

from apps.users.models import User


class UserSerialiser(serializers.ModelSerializer):
    username=serializers.CharField(required=False)

    class Meta:
        model=User
        fields = ['first_name','last_name',"email","password",'username']

    def create(self,validated_data):
        object=self.Meta.model
        new_user = object.objects.create_user(**validated_data)
        return new_user








class UserList(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=['id','full_name']


    def get_full_name(self,obj):
     return " ".join((obj.first_name,obj.last_name))
