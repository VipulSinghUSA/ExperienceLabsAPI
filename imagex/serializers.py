# serializers.py

from rest_framework import serializers

from .models import ClientPkg, Accounting


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ClientPkgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPkg
        fields = '__all__'



class AccountingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounting
        fields = '__all__'
