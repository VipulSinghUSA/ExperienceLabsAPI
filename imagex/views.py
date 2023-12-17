from rest_framework.permissions import IsAuthenticated

from .serializers import LoginSerializer, ClientPkgSerializer, AccountingSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserloginExp, ClientPkg, Accounting, ClientContact, Client
from common.rest_utils import build_response

class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = UserloginExp.objects.using('default').get(email=email)
            refresh = RefreshToken.for_user(user)
            client_contact_id = user.client_contact_id

            client_contact = ClientContact.objects.using('default').get(id=client_contact_id)
            client = Client.objects.using('default').get(id= client_contact.clientid_id)
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
                    # Include other fields as needed
                }

                return build_response(
                    status.HTTP_200_OK,
                    "Success",
                    data={
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'client_contact': client_data,
                        'user_data': user_data,
                    }
                )
            return build_response(
                status.HTTP_400_BAD_REQUEST,
                "Client Id not found",
            )

        except UserloginExp.DoesNotExist:
            return build_response(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid credentials",
            )


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


class AccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, client_id, *args, **kwargs):
        try:
            status_param = request.query_params.get('account_status', None)
            account_status = status_param.lower() == 'true' if status_param is not None else None
            account_objs = Accounting.objects.using('second_db').filter(client_id=client_id)
            account_objs = account_objs.filter(status=account_status)
            status_count = account_objs.count()
            serializer = AccountingSerializer(account_objs, many=True)

            return build_response(
                status.HTTP_200_OK,
                "Success",
                data={
                    'success_record': status_count,
                }
            )
        except Exception as e:
            return build_response(
                status.HTTP_404_NOT_FOUND,
                "Invalid client id",
            )



