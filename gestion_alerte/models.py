from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError(_("The username must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES =(
        ('admin', 'Admin'),
        ('alarmeur', 'Alarmeur'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=50)
    username = models.CharField(_("username"), unique=True, max_length=50)
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now) 

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
      verbose_name = "user"

    def __str__(self):
        return self.username

class Capture(models.Model):
    url = models.CharField(max_length=50, null=True, blank=True, default='')
    base64 = models.TextField(default="") 
    create_date = models.DateTimeField(auto_now_add=True)
    

class Alerte(models.Model):
    capture = models.ForeignKey(Capture, on_delete=models.CASCADE)
    taux = models.FloatField(default=0)
    etat = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.create_date)