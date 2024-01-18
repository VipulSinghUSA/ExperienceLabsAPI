from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
# from account.models import Client,Location



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
#
class Accounting(models.Model):
    accounting_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
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






#

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         return self.create_user(email, password, **extra_fields)
#
# class UserloginExp(AbstractBaseUser):
#     email = models.TextField(blank=True, null=True)
#     password = models.TextField(blank=True, null=True)
#     client_contact = models.ForeignKey(ClientContact, models.DO_NOTHING, blank=True, null=True)
#     active = models.BooleanField(blank=True, null=True)
#     lastlogin = models.DateField(blank=True, null=True)
#     ispwdchange = models.BooleanField(blank=True, null=True)
#     # isadmin = models.BooleanField(db_column='isAdmin', blank=True, null=True)  # Field name made lowercase.
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.email
#
#     # class Meta:
#     #     db_table = 'imagex_userloginexp'
#
#     class Meta:
#         # managed = False
#         db_table = 'userlogin_exp'



