from rest_framework.serializers import ModelSerializer
from authentication.models import User, VerificationCode
from .utils import SaveUserAction

class FindUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
        
        

class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "password"]
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        SaveUserAction(
            user = user,
            action="Account created",
            visible=True,
            action_type="success"
        ).start()
        return user