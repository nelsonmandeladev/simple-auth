
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('simple-auth-admin/', admin.site.urls),
    path("api/v1/auth/", include("api.v1.auth.urls")),
    path("api/v1/users/", include("api.v1.users.urls")),
    path("api/v1/logs/", include("api.v1.logs.urls")),
    path("api/v1/devices/", include("api.v1.devices.urls")),
]
