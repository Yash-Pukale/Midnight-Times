from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    use_in_migration = True

    """
        Creates a new user with the given email and password. If no password is provided, a default password
        will be generated. Raises a ValueError if no email is provided.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields (dict): Additional fields to be included in the user model.

        Returns:
            User
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a new user with the given email and password. If no password is provided, a default password
        will be generated. Raises a ValueError if no email is provided.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields (dict): Additional fields to be included in the user model.

        Returns:
            User
        """
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a new superuser with the given email and password. 
        If no password is provided, a default password will be generated. 
        Ensures that the superuser has 'is_staff=True' and 'is_superuser=True'.
        
        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields (dict): Additional fields to be included in the superuser model.
        
        Returns:
            User: The newly created superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email