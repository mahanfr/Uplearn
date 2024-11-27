from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# This is a class for managing our custom user authentication
class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, user_name, password,
                         **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('SuperUser must be assigned to is_staff'))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('SuperUser must be assigned to is_superuser'))

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password,
                    **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


# This class created to add and replace some features
# of default django user model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=80, unique=True)
    user_name = models.CharField(max_length=80, unique=True)
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_vertified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    vertified_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']
    

# Addition to user model for more inforamtion about user
class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'M', _("male")
        FEMALE = 'F', _("female")
        OTHER = 'O', _("other")

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    bio = models.CharField(max_length=256, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GenderChoices,
                              null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.user_name} Profile'
