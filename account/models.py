# Create your models here.
import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class Client(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'client'


class Location(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    id = models.CharField(primary_key=True, max_length=36,auto_created=True)
    client = models.ForeignKey(Client, models.DO_NOTHING)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'location'
        
        
class ClientContact(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    rep_name = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    cell_no = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    clientid = models.ForeignKey(Client, models.DO_NOTHING, db_column='clientid', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    taxid = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'client_contact'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        extra_fields.setdefault('is_active', True)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password=password, **extra_fields)


class UserloginExp(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.TextField(unique=True)
    password = models.TextField(blank=True, null=True)
    client_contact = models.ForeignKey(ClientContact, models.DO_NOTHING, blank=True, null=True)
    active = models.BooleanField(default=True)
    lastlogin = models.DateField(blank=True, null=True)
    ispwdchange = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email


    class Meta:
        # managed = False
        db_table = 'userlogin_exp'
        
        

class ClientExplabs(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)

    name = models.TextField(blank=True, null=True)
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    zipcode = models.TextField(blank=True, null=True)
    client_type = models.TextField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    imagex_client_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'client_explabs'



class ClientLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    loc_name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    imagex_location_id = models.CharField(max_length=255, blank=True, null=True)
    imagex_client_id = models.CharField(max_length=255, blank=True, null=True)
    imagex_api_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'client_location'
        
        
class ClientPkg(models.Model):
    id = models.IntegerField(primary_key=True)
    compid = models.ForeignKey(ClientExplabs, models.DO_NOTHING, db_column='compid', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    billing_type = models.TextField(db_column='billing-type', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    pkg = models.ForeignKey('Subscription', models.DO_NOTHING, blank=True, null=True)
    credits = models.BigIntegerField(blank=True, null=True)
    balance = models.BigIntegerField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'client_pkg'
        
        
        
class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    pkg_name = models.TextField(blank=True, null=True)
    cost_per_credits = models.TextField(blank=True, null=True)
    minimum_credits = models.TextField(blank=True, null=True)
    reorder_level = models.TextField(db_column='reorder-level', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    active = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_saas = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'subscription'
        
        
from rest_framework import serializers   
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    
    

class Country(models.Model):
    name = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'country'