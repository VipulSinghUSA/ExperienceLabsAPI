from django.db import ProgrammingError
from .serializers import AccountingSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import  Accounting
from common.rest_utils import build_response



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
