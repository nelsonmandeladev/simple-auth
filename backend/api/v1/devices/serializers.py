from rest_framework.serializers import ModelSerializer
from authentication.models import UserDevices

class UsersDevicesSerializer(ModelSerializer):
    class Meta: 
        model = UserDevices
        fields = "__all__"