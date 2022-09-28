from authentication.models import User, UsersActions
from rest_framework.generics import ListAPIView
from .serializers import (
    UserListSerializer, 
    UserSerializer, 
)
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from api.v1.auth.utils import SaveUserAction, EmailVerification

class ListUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAdminUser, )
    
class UserView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, user_id = None):
        if user_id is None:
            return Response(
                {
                    "detail": "User id must be provided"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id = user_id, as_deleted = False)
            serializer = self.serializer_class(user, many = False)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
            {
                "detail": f"User with Id: {user_id} does not exist"
            },
            status=status.HTTP_404_NOT_FOUND
        )
            
    def delete(self, request, user_id = None):
        if user_id is None:
            return Response(
                {
                    "detail": "User Id must be provided"
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(id = user_id, as_deleted = False)
            user.as_deleted = True
            SaveUserAction(
                user = user,
                action = f"User account with Id: {user_id} deleted",
                action_type = "danger",
                visible = False
            ).start()
            user.save()
            return Response(
                {
                    "detail": f"User with Id: {user_id} has been deleted"
                },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {
                    "detail": f"User with Id: {user_id} does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, user_id = None):
        if user_id is None:
            return Response(
                {
                    "detail": "User Id must be provided"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        user = None
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(id = user_id, as_deleted = False)
        except User.DoesNotExist:
            return Response(
                {
                    "detail": f"User with Id: {user_id} does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if email:
            user.email = email
            user.is_verified = False
            user_action = SaveUserAction(
                user = user,
                action = f"Email changed to {email}",
                action_type = "info"
            )
            user.save()
            user_action.start()    
            return Response(
                {
                    "detail": f"Email for user with Id {user_id} has been changed"
                },
                status=status.HTTP_200_OK
            )
                
        if password:
            user.set_password(password)
            user_action = SaveUserAction(
                user = user,
                action = "Password changed",
                action_type = "info"
            )
            user.save()
            user_action.start()
            return Response(
                {
                    "detail": f"Password for user with Id {user_id} has been changed"
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            {
                "detail": "You should provide at least one valid parameter"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
                