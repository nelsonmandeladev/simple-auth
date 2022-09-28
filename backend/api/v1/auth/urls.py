from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh-token'),
    path('find', views.findUser, name='find-user'),
    path('verify', views.verifyUser, name='verify-user'),
    path("send-code", views.sendCode, name="send-code"),
    path("2fa", views.twoFactorAuthentication, name='2fa')
]