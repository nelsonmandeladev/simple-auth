from django.urls import path
from .import views 

urlpatterns = [
    path("", views.ListUserActionView.as_view(), name="logs"),
    path("<str:user_id>", views.userActionView, name="user-logs")
]