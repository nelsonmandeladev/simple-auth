from rest_framework.generics import ListAPIView
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import UsersDevicesSerializer
from authentication.models import User, UserDevices

class DevicesListView(ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = UsersDevicesSerializer
    queryset = UserDevices.objects.all()

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, ])
def userDevicesListView(request, user_id = None):
    if user_id is None:
        return Response(
            {
                "detail": "User Id must be provided"
            },
            status= status.HTTP_400_BAD_REQUEST
        )
    
    user = None
    try:
        user = User.objects.get(
            id = user_id,
            as_deleted = False
        )
    except User.DoesNotExist:
        return Response(
            {
                "detail": f"User with Id: {user_id} does not exist"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    user_devices = UserDevices.objects.filter(
        user = user
    )
    
    serializer = UsersDevicesSerializer(user_devices, many = True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )