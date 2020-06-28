from django.conf.urls import url
from kizen_user.views.v1 import auth, register

urlpatterns = [
    url(r'login/', auth.LoginAPIView.as_view(), name="login user"),
    url(r'logout/', auth.LogoutAPIView.as_view(), name="logout user"),
    url(r'register/', register.RegisterAPIView.as_view(), name="register user"),
]
