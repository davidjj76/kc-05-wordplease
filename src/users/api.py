from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blogs.models import Blog
from blogs.serializers import BlogSerializer
from users.permissions import UserPermission
from users.serializers import UserSerializer


class UsersAPI(APIView):


    def post(self, request):
        """
        Creates a user
        :param request: HttpRequest object
        :return: HttpResponse object
        """
        user_serializer = UserSerializer(data=request.data)
        blog_serializer = BlogSerializer(data=request.data)
        if user_serializer.is_valid() and blog_serializer.is_valid():
            username = user_serializer.data.get('username')
            password = user_serializer.data.get('password')
            email = user_serializer.data.get('email')
            first_name = user_serializer.data.get('first_name')
            last_name = user_serializer.data.get('last_name')
            blog_title = blog_serializer.data.get('title')

            User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                blog=Blog(title=blog_title)
            )
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
