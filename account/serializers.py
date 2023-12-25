from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *

User = get_user_model()


class UserloginExpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserloginExp
        fields = '__all__'

class ClientExplabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientExplabs
        fields = ('name', 'imagex_client_id')


class LocationSerializer(serializers.ModelSerializer):
  class Meta:
        model = ClientLocation
        fields = ('description', 'imagex_client_id','imagex_location_id','imagex_api_key','loc_name')
        
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ClientPkgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPkg
        fields = '__all__'
        
        
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']
        
class ClientLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLocation
        fields =  ["id","loc_name","description","imagex_location_id","imagex_client_id","imagex_api_key"]
        
        
class ClientContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientContact
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    client_contact = ClientContactSerializer()

    class Meta:
        model = UserloginExp
        fields = ['id', 'email', 'is_superuser', 'client_contact']