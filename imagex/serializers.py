# serializers.py

from rest_framework import serializers

from .models import Accounting,Location




class AccountingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounting
        fields = '__all__'


class RecordLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserloginExp
#         fields = ('email', 'password', 'client_contact')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = UserloginExp.objects.using('default').create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             client_contact=validated_data['client_contact']
#             # Add other fields as needed
#         )
#         return user


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserloginExp
#         fields = ('email', 'password', 'client_contact')



