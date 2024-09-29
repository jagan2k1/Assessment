from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    user_id = models.CharField(primary_key=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    is_staff = models.IntegerField()
    is_superuser = models.IntegerField()
    is_active = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    profile = models.JSONField()
    status = models.IntegerField()
    settings = models.JSONField(blank=True, null=True)
    is_verified = models.IntegerField()
    created_at = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["password"]
    objects = UserManager()

    class Meta:
        db_table = 'User'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    product_details = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
