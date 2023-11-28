from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("me/", views.UserAPIView.as_view(), name="user-info"),
]
app_name = "user"
