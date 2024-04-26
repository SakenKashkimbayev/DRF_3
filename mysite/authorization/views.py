from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from rest_framework.response import Response

from authorization.models import User
from authorization.serializers import LoginSerializer, RegistrationSerializer


# Create your views here.
class LoginView(generics.GenericAPIView):
    queryset = User.object.all()
    serializer_class = LoginSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response("detail: login")
        return Response("detail: Error")


class LogoutView(generics.GenericAPIView):
    queryset = User.object.all()
    serializer_class = LoginSerializer
    def get(self, request):
        logout(request)
        return Response("detail: logget out")

class RegistrationView(generics.CreateAPIView):
    queryset = User.object.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("detail: User create")
        return Response("detail: Error")

