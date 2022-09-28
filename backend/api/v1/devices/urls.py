from django.urls import path
from . import views

urlpatterns = [
    path("", views.DevicesListView.as_view(), name="devices"),
    path("<str:user_id>", views.userDevicesListView, name="user-devices")
]