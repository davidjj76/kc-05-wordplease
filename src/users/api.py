from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import UserSerializer, UsersListSerializer


class UsersAPI(APIView):

    def get(self, request):
        """
        Returns a list of system users
        :param request: HttpRequest object
        :return: HttpResponse object
        """
        username = request.query_params.get('username', '')
        order = request.query_params.get('order', '')
        order_by = '-username' if order == 'des' else 'username'
        users = User.objects.all().values('id', 'username')\
            .filter(username__startswith=username)\
            .order_by(order_by)
        serializer = UsersListSerializer(users, many=True, context= { 'request': request })
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):
    """
    User detail (GET), user update (PUT), user delete (DELETE)
    """

    def get(self, request, pk):
        """
        Returns a user detail
        :param request: HttpRequest object
        :param pk: user pk
        :return: HttpResponse object
        """
        user = get_object_or_404(User, pk=pk)
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
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
