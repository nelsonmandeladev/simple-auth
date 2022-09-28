from ast import Return
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from authentication.models import (
    User,
    UserDevices,
    VerificationCode
)
from .serializers import UsersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .utils import (
    SaveUserAction,
    EmailVerification,
    SendCode,
    checkCode
)


@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def register(request):
    data = request.data
    origin =request.headers.get("Origin")
    email = data.get("email")
    password = data.get("password")
    
    if email is None or password is None:
        return Response(
            {
                "detail": "The user email and password are required in other to make this request"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    request.headers.get("Origin")
    if User.objects.filter(email = email, as_deleted = False).exists():
        return Response(
            {
                "detail": f"User account with email: {email} already exists"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = UsersSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email = serializer.data.get("email"))
        EmailVerification(user, origin).start()
        response_data = {
            "id" : serializer.data["id"],
            "email" : serializer.data["email"],
        }
        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )

@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def findUser(request):
    data = request.data
    user = None
    email = data.get("email")
    if email is None:
        return Response(
            {
                "detail": "User email must be provided"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        return Response(
            {
                "detail": f"User with email {email} does not exist"
            },
            status = status.HTTP_404_NOT_FOUND
        )
    
    if user:
        EmailVerification(user).start()
        SaveUserAction(
            user = user,
            action="Account luck up",
            action_type="info"
        ).start()
        return Response(
            {
                "detail": f"Code for user with Email {email} has been sended"
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "detail": f"User with email {email} does not exist"
        },
        status = status.HTTP_404_NOT_FOUND
    )

@api_view(["POST"])
@permission_classes([permissions.AllowAny,])
def login(request) :
    data = request.data
    email = data["email"]
    password = data["password"]
    user = None
    
    try:
        user = User.objects.get(email = email, as_deleted = False)
    except User.DoesNotExist:
        return Response(
            {
                "detail:": "User with provides credential does not exist"
            },
            status = status.HTTP_404_NOT_FOUND
        )
    
    authenticate_user = authenticate(
        email = email,
        password = password
    )
    
    if authenticate_user:
        refresh = RefreshToken.for_user(
            authenticate_user
        )
        user_device = None
        try:
            user_device = UserDevices.objects.get(
                user = user,
                name = request.user_agent.device.family,
                os = str(request.user_agent.os.family),
                browser = str(request.user_agent.browser.family ),
                agent = str(request.user_agent)
            )
        except UserDevices.DoesNotExist:
            user_device = UserDevices.objects.create(
                user = user,
                name = request.user_agent.device.family,
                os = str(request.user_agent.os.family),
                browser = str(request.user_agent.browser.family ),
                agent = str(request.user_agent)
            )
            user_device.save()
        SaveUserAction(
            user = user,
            action = "logging attempt success",
            action_type= "success"
        ).start()
        response_data = {
            "user" : {
                "id": user.id,
                "email": user.email,
                "is_verified": user.is_verified,
                "two_factor_auth": user.two_factor_auth,
            },
            "token":{
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            "device":{
                "name": user_device.name,
                "os": user_device.os,
                "browser": user_device.browser,
                "agent": user_device.agent
            }
        }
        return Response(
            data=response_data,
            status=status.HTTP_201_CREATED
        )
        
    SaveUserAction(
        user = user,
        action = "Logging attempt failed",
        action_type = "danger"
    ).start()
    return Response(
        {
            "detail": "User with provides credential does not exist"
        },
        status=status.HTTP_403_FORBIDDEN
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny, ])
def verifyUser(request):
    data = request.data
    code = data.get("code")
    user_email = data.get("email")
    channel = data.get("channel")
    device_id = data.get("device_id")
    
    if channel is None or code is None:
        return Response(
            {
                "detail": "The channel, and the verification code should be provided in order to perform this request"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = None
    try:
        user = User.objects.get(
            email = user_email,
            as_deleted = False
        )
    except User.DoesNotExist:
        return Response(
            {
                "detail:": f"User with email: {user_email} does not exist"
            },
            status = status.HTTP_404_NOT_FOUND
        )
        
    if user:
        if channel == "email" and user_email is not None:
            try:
                code = VerificationCode.objects.get(
                    account = user,
                    code = code,
                    is_used = False,
                    expired = False
                )
                user.is_verified = True
                code.is_used = True
                user.save()
                code.save()
                return Response(
                    {
                        "detail": f"User with email: {user_email} has been verified with code: {code.code}"
                    },
                    status=status.HTTP_200_OK
                )
            except VerificationCode.DoesNotExist:
                return Response(
                    {
                        "detail": "This code does not exist or has been expired"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        
        if channel == "sms" and  device_id is not None:
            code_status = checkCode(phone=user.phone, code=code)
            if code_status == "approved":
                device = UserDevices.objects.get(
                    user = user,
                    id = device_id
                )
                device.is_verified = True
                device.save()
                return Response(
                    {
                        "detail": f"Code {code} approved"
                    },
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {
                    "detail": f"Code {code} rejected: May be incorrect or expired"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        
        return Response(
            {
                'detail' : "And error occurred, make sure to provide the good channel, user_email, code and device_id if it's a sms verification"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
            

@api_view(["POST"])
@permission_classes([permissions.AllowAny, ])
def sendCode(request):
    data = request.data
    user_email = data.get("email")
    code_channel = data.get("channel")
    phone_number = data.get("phone")
    
    if code_channel is None:
        return Response(
            {
                "detail": "The channel should be provided in other to send code for this user"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
               
    if code_channel == "email":
        if user_email:
            try:
                user = User.objects.get(email = user_email, as_deleted = False)
                EmailVerification(user).start()
                user.is_verified = False
                user.save()
                return Response(
                    {
                        "detail": f"Verification code for user with email: {user_email} has been sended"
                    },
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {
                        "detail": f"User with email: {user_email} does not exists"
                    },
                    status = status.HTTP_404_NOT_FOUND
                )
        return Response(
            {
                "detail": "The user email should be provided in other to process for this user"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if code_channel == "sms":
        if phone_number:
            send_code = SendCode(phone_number)
            send_code.start()
            return Response(
                {
                    "detail": f"Code for user with phone {phone_number} has been sended"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "detail": "The user phone number should be provided in other send code"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(
        {
            "detail": "Make sure to provide the correct requested data"
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, ])
def twoFactorAuthentication(request):
    data = request.data
    user_id = data.get("user_id")
    phone_number = data.get("phone")
    
    if user_id is None or phone_number is None:
        return Response(
            {
                "detail": "The enable 2fa for this user, user_id and phone must be provide"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(
            id = user_id,
            as_deleted = False
        )
        
        if user.two_factor_auth == True:
            return Response(
                {
                    "detail": "2FA for this user is already enabled"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.phone = phone_number
        user.two_factor_auth = True
        send_code = SendCode(phone_number)
        user_action = SaveUserAction(
            user=user,
            action="Two factor authentication enabled",
            action_type="info"
        )
        user.save()
        send_code.start()
        user_action.start()
        return Response(
            {
                "detail": f"2FA for user with id {user_id} enabled"
            },
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {
                "detail": f"User with id: {user_id} does not exists"
            },
            status = status.HTTP_404_NOT_FOUND
        )