from authentication.models import User, UsersActions
from rest_framework.serializers import ModelSerializer


class UserListSerializer(ModelSerializer):
    class Meta: 
        model = User
        exclude = [
            "password", 
            "groups", 
            "user_permissions", 
        ]

class UserSerializer(ModelSerializer):
    class Meta: 
        model = User
        exclude = [
            "password", 
            "groups", 
            "user_permissions", 
            "as_deleted",
            "update_action"
        ]

class UpdateUserSerializer(ModelSerializer):
    model = User
    fields = [
        "id", 
        "email", 
        "password", 
    ]
