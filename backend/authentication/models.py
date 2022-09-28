from hashlib import blake2b
from operator import le
import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUSerManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The User Email should be provided'))
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))


        return self.create_user(email,password,**extra_fields)

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username=None
    first_name = None
    last_name = None
    email=models.CharField(
        _('Email'), 
        max_length=255,
        unique=True, 
        null=True, 
        blank=True
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    as_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    two_factor_auth = models.BooleanField(default=False)
    date_joined=models.DateTimeField(_('Date'),auto_now_add=True, null=True, blank=True)
    last_update = models.DateTimeField(_('LastUpdate'), auto_now=True, null=True, blank=True)


    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'
    
    objects = CustomUSerManager()
    
    class Meta:
        verbose_name = 'User account'
        verbose_name_plural = 'User account'

    def __str__(self):
        return self.email
    
class VerificationCode(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    account = models.ForeignKey(
        User,
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    code = models.UUIDField(
        null=True,
        blank=False,
        unique=True,
        default=uuid.uuid4
    )
    is_used = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    
    date_create = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True
    )
    last_update = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"
    
    def __str__(self):
        return str(self.code)

class UsersActions(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    ACTION_TYPE = (
        ("success", "success"),
        ("danger", "danger"),
        ("info", "info"),
        ("warning", "warning")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    action_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=ACTION_TYPE
    )
    visible = models.BooleanField(default=True)
    action = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    last_update = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "User Action"
        verbose_name_plural = "Users Actions"
    
    def __str__(self):
        return str(self.id)

class UserDevices(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    os = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    browser = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    agent = models.TextField(
        max_length=5000,
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False)
    date_create = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    last_update = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True
    )
    class Meta:
        verbose_name = "User Device"
        verbose_name_plural = "Users Devices"
    
    def __str__(self):
        return str(self.id)