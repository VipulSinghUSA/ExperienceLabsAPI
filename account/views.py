import json
import uuid

import requests
from common.rest_utils import build_response
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

User = get_user_model()  


class UserRegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        email = data['email']
        email = email.lower()
        password = data['password']
        cell_no = data['cell_no']
        designation = data['designation']
        imagex_client_id = data['imagex_client_id']
        first_name = data['first_name']
        last_name = data['last_name']
        try:
            if imagex_client_id:
                client = Client.objects.get(id = imagex_client_id)
            client_contact = ClientContact.objects.create(cell_no=cell_no,last_name=last_name,first_name=first_name,designation=designation,clientid=client,email=email)
        except ClientContact.DoesNotExist:
            return build_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Error creating ClientContact",
                data=None
            )
            
        user_model = get_user_model()
        user = user_model.objects.create_user(email=email, password=password)
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        client_contact=client_contact,
        user.save()
        serializer = UserloginExpSerializer(user)
        return build_response(
            status.HTTP_200_OK,
            "Success",
            data=serializer.data
        )
        
class ClientExplabsAPIView(APIView):
    def post(self, request,client_id, *args, **kwargs):
        api_url = f'https://dxmltpiz2ac2inuhad3au4ugqa0pbtqe.lambda-url.us-east-1.on.aws/admin/location/{client_id}/'
        headers = {
            'accept': 'application/json',
            'x-api-key': '6221c617-1380-4912-88eb-ba737be2b8ce',
            'Content-Type': 'application/json',
        }
        payload = request.data
        data=json.dumps(payload)

        try:
            response = requests.post(api_url, data=data, headers=headers)
            response.raise_for_status()
            data = response.json()
            client = ClientExplabs.objects.create(
                name=data.get('name'),
                imagex_client_id=data.get('id')
            )


            serializer = ClientExplabsSerializer(client)
            return build_response(
                status.HTTP_200_OK,
                "Success",
                data=serializer.data
            )
        except requests.RequestException as e:
            return Response({'error': f'Error updating clients: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        



class LocationAPIView(APIView):
    def post(self, request,client_id,*args, **kwargs):
        api_url = f'https://dxmltpiz2ac2inuhad3au4ugqa0pbtqe.lambda-url.us-east-1.on.aws/admin/location/{client_id}/'
        headers = {
            'accept': 'application/json',
            'x-api-key': '6221c617-1380-4912-88eb-ba737be2b8ce',
            'Content-Type': 'application/json',
        }
        payload = request.data
        data=json.dumps(payload)

        try:
           
            response = requests.post(api_url, data=data, headers=headers)
            response.raise_for_status()
            data = response.json()
            client_id = data['client_id']
            
            client = Client.objects.get(id=client_id)
            location = ClientLocation.objects.create(
                loc_name=data.get('name'),
                description=data.get('description'),
                imagex_api_key=data.get('api_key'),
                imagex_client_id=data.get('client'),
                imagex_location_id = str(uuid.uuid4())
            )
            serializer = LocationSerializer(client)
            return build_response(
                status.HTTP_200_OK,
                "Success",
                data=serializer.data
            )

        except requests.RequestException as e:
            return Response({'error': f'Error updating clients: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
# class UserLoginAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
        
#         try:

#             user = UserloginExp.objects.get(email=email)
          
#             refresh = RefreshToken.for_user(user)
#             client_contact_id = user.client_contact_id

#             client_contact = ClientContact.objects.using('default').get(id=client_contact_id)
#             client = Client.objects.using('default').get(id=client_contact.clientid_id)
#             if client:
#                 client_data = {
#                     'id': client.id,
#                     'name': client.name,
#                     'description': client.description,
#                     'created_at': client.created_at,
#                     'updated_at': client.updated_at,

#                 }
#                 user_data = {
#                     'id': user.id,
#                     'email': user.email,
#                     'active': user.active,
#                     'lastlogin': user.lastlogin,
#                     'ispwdchange': user.ispwdchange,
#                     # Include other fields as needed
#                 }

#                 return build_response(
#                     status.HTTP_200_OK,
#                     "Success",
#                     data={
#                         'access_token': str(refresh.access_token),
#                         'refresh_token': str(refresh),
#                         'client_contact': client_data,
#                         'user_data': user_data,
#                     }
#                 )
#             return build_response(
#                 status.HTTP_400_BAD_REQUEST,
#                 "Client Id not found",
#             )

#         except UserloginExp.DoesNotExist:
#             return build_response(
#                 status.HTTP_401_UNAUTHORIZED,
#                 "Invalid credentials",
#             )

class ClientPkgAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id, *args, **kwargs):
        try:
            client_packages = ClientPkg.objects.filter(client_id=client_id)
            serializer = ClientPkgSerializer(client_packages, many=True)
            return build_response(
                status.HTTP_200_OK,
                "Success",
                data=serializer.data
            )
        except Exception as e:
            return build_response(
                status.HTTP_404_NOT_FOUND,
                "Invalid client  id",
            )
            


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            client_contact_id = user.client_contact_id

            if user:
                user = UserloginExp.objects.get(email=email)
                client_contact = ClientContact.objects.using('default').get(id=client_contact_id)
                client = Client.objects.using('default').get(id=client_contact.clientid_id)
                if client:
                    client_data = {
                        'id': client.id,
                        'name': client.name,
                        'description': client.description,
                        'created_at': client.created_at,
                        'updated_at': client.updated_at,

                    }
                    user_data = {
                        'id': user.id,
                        'email': user.email,
                        'active': user.active,
                        'lastlogin': user.lastlogin,
                        'ispwdchange': user.ispwdchange,
                    }
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)
                    data = {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        "user_data" : user_data,
                        "client_data":client_data
                    }

                    return build_response(
                        status.HTTP_200_OK,
                        "Login Successfully",
                        data = data
                    )
            return build_response(
                status.HTTP_404_NOT_FOUND,
                "Failed",
                data=None,
                errors =  "Invalid credentials"
            )

        except Exception as e:
            return build_response(
                status.HTTP_400_BAD_REQUEST,
                "Invalid credentials",
            )
            


class CountryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            countries = Country.objects.all()
            serializer = CountrySerializer(countries, many=True)
            return build_response(
                        status.HTTP_200_OK,
                        "Success",
                        data = serializer.data,
                     
                    )
        except Exception as e:
            return build_response(
                status.HTTP_400_BAD_REQUEST,
                "Failed",
                data = None
            )
            
            
# class LocationListAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         breakpoint()
#         try:
            
#             client_location = ClientLocation.objects.all()
#             serializer = ClientLocationSerializer(client_location, many=True)
#             return build_response(
#                 status.HTTP_200_OK,
#                 "Success",
#                 data=serializer.data,
#             )
#         except Exception as e:
#             return build_response(
#                 status.HTTP_400_BAD_REQUEST,
#                 "Failed",
#                 data=None,
#             )
            
class UserProfileAPIView(APIView):
    def get(self, request ,*args, **kwargs):
        try:
            user = request.user  
            serializer = UserProfileSerializer(user)
            return build_response(
                status.HTTP_200_OK,
                "Success",
                data=serializer.data,
            )
            
        except Exception as e:
            return build_response(
                status.HTTP_400_BAD_REQUEST,
                "Failed",
                data=None,
            )
            
class LocationListAPIView(APIView):
     def get(self, request ,*args, **kwargs):
        try:
            breakpoint()
            client_location = ClientLocation.objects.all()
            serializer = ClientLocationSerializer(client_location, many=True)
            return build_response(
                status.HTTP_200_OK,
                "Success",
                data=serializer.data,
            )
            
        except Exception as e:
            return build_response(
                status.HTTP_400_BAD_REQUEST,
                "Failed",
                data=None,
            )
    