from django.urls import path

from api.v1.users.views import GoogleLoginAPIView, LogoutAPIView, MeAPIView

urlpatterns = [
    path("google/login/", GoogleLoginAPIView.as_view(), name="google-login"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
