from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authorization.views import LoginView, LogoutView, RegistrationView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('registration/', RegistrationView.as_view()),

    path('token/', TokenObtainPairView.as_view()),
    path('logout/refresh/', TokenRefreshView.as_view()),
    ]

