from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.permissions import UserPermission
from users.serializers import UserSerializer


class UsersAPI(APIView):

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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):
    """
    User detail (GET), user update (PUT), user delete (DELETE)
    """
    permission_classes = (UserPermission,)

    def get(self, request, pk):
        """
        Returns a user detail
        :param request: HttpRequest object
        :param pk: user pk
        :return: HttpResponse object
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Updates a user
        :param request: HttpRequest object
        :param pk: user pk
        :return: HttpResponse object
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deletes a user
        :param request: HttpRequest object
        :param pk: user pk
        :return: HttpResponse object
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
