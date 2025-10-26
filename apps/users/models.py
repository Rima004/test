from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps
# Create your models here.



class Manager(UserManager):



    def _create_user_object(self, username, email, password, **extra_fields):

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        return user



class User(AbstractUser):
    first_name=models.CharField(max_length=20)
    last_name =models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)


    username = models.CharField(
        _("username"),null=True,
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()]
    )
    objects = Manager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
