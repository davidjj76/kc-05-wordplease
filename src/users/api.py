from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import UserSerializer


class UsersAPI(APIView):

    def get(self, request):
        """
        Return a list of system users
        :param request: HttpRequest object
        :return: HttpResponse object
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a user
        :param request: HttpRequest object
        :return: HttpResponse object
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
