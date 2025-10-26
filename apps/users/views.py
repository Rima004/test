from logging import raiseExceptions

from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import UserSerialiser, UserList
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
# Create your views here.


class RegisterUser(APIView):
    serializer_class = UserSerialiser
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            refresh=RefreshToken.for_user(new_user)

            return Response({

                'refresh': str(refresh),

                'access': str(refresh.access_token),

            })



class ListUsers(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserList


