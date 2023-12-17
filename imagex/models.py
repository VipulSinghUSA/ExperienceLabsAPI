from django.contrib.auth.base_user import BaseUserManager
from django.db import models


#
class Accounting(models.Model):
    accounting_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    error = models.CharField(max_length=255, blank=True, null=True)
    ort_session_time = models.FloatField(blank=True, null=True)
    matting_time = models.FloatField(blank=True, null=True)
    main_operation_time = models.FloatField(blank=True, null=True)
    image_download_time = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'accounting'


class Client(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'client'


class ClientContact(models.Model):
    id = models.IntegerField(primary_key=True)
    rep_name = models.TextField(blank=True, null=True)
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


class ClientExplabs(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    zipcode = models.TextField(blank=True, null=True)
    client_type = models.TextField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'client_explabs'


class ClientLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    loc_name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    copanyid = models.ForeignKey(ClientExplabs, models.DO_NOTHING, db_column='copanyid', blank=True, null=True)

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


class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    client = models.ForeignKey(Client, models.DO_NOTHING)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'location'


#
#
class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    pkg_name = models.TextField(blank=True, null=True)
    cost_per_credits = models.TextField(blank=True, null=True)
    minimum_credits = models.TextField(blank=True, null=True)
    reorder_level = models.TextField(db_column='reorder-level', blank=True,
                                     null=True)  # Field renamed to remove unsuitable characters.
    active = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_saas = models.BooleanField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'subscription'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class UserloginExp(models.Model):
    email = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    client_contact = models.ForeignKey(ClientContact, models.DO_NOTHING, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    lastlogin = models.DateField(blank=True, null=True)
    ispwdchange = models.BooleanField(blank=True, null=True)
    # isadmin = models.BooleanField(db_column='isAdmin', blank=True, null=True)  # Field name made lowercase.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # class Meta:
    #     db_table = 'imagex_userloginexp'

    class Meta:
        # managed = False
        db_table = 'userlogin_exp'


