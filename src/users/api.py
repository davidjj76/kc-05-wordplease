from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer


class UsersAPI(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
