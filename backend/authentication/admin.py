from django.contrib import admin
from .models import UserDevices, UsersActions, User, VerificationCode

# Register your models here.
admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(UsersActions)
admin.site.register(UserDevices)