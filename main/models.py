from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .choices import DEPARTAMENTO
from django.contrib.auth import get_user_model


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not extra_fields.get('name'):
            raise ValueError('The Name must be set')
        if not password:
            raise ValueError('The Password must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=150, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=150, blank=True, null=True)
    apellido_materno = models.CharField(max_length=150, blank=True, null=True)
    departamento = models.PositiveSmallIntegerField(choices=DEPARTAMENTO, blank=True, null=True)

    def nombre_completo(self):
        return f'{self.apellido_paterno}{self.apellido_materno}{self.nombre}'
    
    class Meta:
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    