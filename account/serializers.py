from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import ClientExplabs,Location,ClientContact,ClientPkg,UserloginExp,Country

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
        model = Location
        fields = ('name', 'client','description','api_key')
        
        

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