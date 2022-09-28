from authentication.models import UsersActions
from rest_framework.serializers import ModelSerializer

class UsersActionsListSerializer(ModelSerializer):
    class Meta:
        model = UsersActions
        fields = "__all__"
        
class UsersActionsSerializer(ModelSerializer):
    class Meta:
        model = UsersActions
        exclude = ["user", "visible", "last_update"]