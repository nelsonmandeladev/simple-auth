from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListUsersView.as_view(), name = "users"),
    path("<str:user_id>", views.UserView.as_view(), name="single-user"),
]