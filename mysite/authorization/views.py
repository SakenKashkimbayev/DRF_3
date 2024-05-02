from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from authorization.models import User
from authorization.serializers import LoginSerializer, RegistrationSerializer, PersonalAreaSerializer


# Create your views here.
# class LoginView(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = LoginSerializer
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return Response("detail: login")
#         return Response("detail: Error")
#
#
# class LogoutView(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = LoginSerializer
#     def get(self, request):
#         logout(request)
#         return Response("detail: logget out")

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

class PersonalAreaView(RetrieveAPIView):
    serializer_class = PersonalAreaSerializer

    def get_object(self):
        # Получаем текущего аутентифицированного пользователя
        return self.request.user