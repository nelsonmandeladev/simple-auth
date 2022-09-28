from threading import Thread
from twilio.rest import Client
import time
from authentication.models import UsersActions, VerificationCode
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

account_sid = "your_account_sid"
auth_token = "your_auth_token"
client = Client(account_sid, auth_token)

class SendCode(Thread):
    def __init__(self, phone):
        self.phone = phone
        Thread.__init__(self)

    def run(self):
        try:
            verification = client.verify \
                     .v2 \
                     .services("your_service_id") \
                     .verifications \
                     .create(to=self.phone, channel='sms')

        except Exception as e:
            print(e)


def checkCode(phone, code):
    try:
        check_code = client.verify \
            .v2 \
            .services("your_service_id") \
            .verification_checks \
            .create(to=phone, code=code)
        return check_code.status
    except Exception as e:
        print(e)
    
class SaveUserAction(Thread):
    def __init__(
        self,
        user,
        action:str,
        action_type:str,
        visible:bool|None = True
    ):
        self.user = user
        self.action = action
        self.action_type = action_type
        self.visible = visible
        Thread.__init__(self)
    
    def run(self):
        try:
            user_action = UsersActions.objects.create(
                user = self.user,
                action = self.action,
                action_type = self.action_type,
                visible = self.visible
            )
            user_action.save()
        except Exception as e:
            print(e)

class EmailVerification(Thread):
    def __init__(self, user, origin:str = None):
        self.user = user
        self.origin = origin
        Thread.__init__(self)
        
    def setCodeToExpired(self,code_id):
        code = VerificationCode.objects.get(id = code_id)
        code.expired = True
        code.save()
        
    def run(self) -> None:
        try:
            verification_code = VerificationCode.objects.create(
                account = self.user
            )
            verification_code.save()
            
            subject = "Account Verification"
            
            html_content = f'<p>Your serv-prov verification code is: <strong>{verification_code.code}</strong></p> <p>Your can verify directly by heating <a href="{self.origin}/verify/{verification_code.code}" target="_blank" rel="noopener noreferrer">HERE</a></p>'
            
            email_to_send = EmailMultiAlternatives(
                subject,
                html_content,
                settings.EMAIL_HOST_USER,
                [self.user.email]
            )
            email_to_send.content_subtype = "html"
            email_to_send.send(fail_silently=False)
            time.sleep(60)
            self.setCodeToExpired(verification_code.id)
        except Exception as e:
            print(f"Error {e}")