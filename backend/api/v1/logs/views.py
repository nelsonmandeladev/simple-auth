from rest_framework import permissions
from authentication.models import UsersActions, User
from rest_framework.generics import ListAPIView
from .serializers import UsersActionsListSerializer, UsersActionsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

class ListUserActionView(ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = UsersActionsListSerializer
    queryset = UsersActions.objects.all()


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, ])
def userActionView(request, user_id = None):
    if user_id is None:
        return Response(
            {
                "detail": "User Id must be provided"
            },
            status= status.HTTP_400_BAD_REQUEST
        )
    
    user = None
    try:
        user = User.objects.get(id = user_id, as_deleted = False)
    except User.DoesNotExist:
        return Response(
            {
                "detail": f"User with Id: {user_id} does not exist"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    user_actions = UsersActions.objects.filter(
        user = user,
        visible = True
    )
    
    serializer = UsersActionsSerializer(user_actions, many = True)
    return Response(
        serializer.data,
        status = status.HTTP_200_OK
    )