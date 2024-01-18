import json
import os

import requests
from common.rest_utils import build_response
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import ProgrammingError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Accounting, Client, Location
from .serializers import AccountingSerializer


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


            
class RecordLocationByClientId(APIView):
    def get(self, request, client_id):
        try:
          
            accounting_entries = Accounting.objects.filter(client_id=client_id)
            if not accounting_entries.exists():
                return Response({'error': 'No Accounting entry found for the given client ID'}, status=status.HTTP_404_NOT_FOUND)

            location_entries = []
            for accounting_entry in accounting_entries:
                # Assuming you want data from all related Location entries
                locations = Location.objects.filter(client=accounting_entry.client)
                location_entries.extend(locations)
            
            location_entries = Location.objects.filter(client=accounting_entries.first().client)
            serializer = RecordLocationSerializer(location_entries, many=True)
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

# class RemoveBackgroundAPIView(APIView):
#     # parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         image_file = request.FILES.get('image',None)

#         if image_file:
#             data = request.data
            
#             # temp_file_path = default_storage.save('temp_image.jpg', image_file)
#             # # temp_file_path = os.path.join('media', temp_file_path)
#             temp_file_path = default_storage.save('temp_image.jpg', image_file)
#             temp_file_path = os.path.join(settings.MEDIA_ROOT, temp_file_path)
            
#             image_file.seek(0)
#             image_content = image_file.read()
#             config = json.loads(image_content)
            
#             input_folder = config["inputfolder"]
#             ouput_folder = config["outputfolder"]
#             temp_folder = config["tempfolder"]
            
#             url = 'https://api.pixian.ai/api/v2/remove-background'
#             auth = ('px7cjqhnn9qvelj', 'd11tt5p1s38rqf025shq9j2fljb1a94fntcktubm8b0jcb7853v2')
            
#             for image in os.scandir(input_folder):    
#                 response = requests.post(url, files={'image': open(image.path, 'rb')},
#                                         data=config,
#                                         auth=auth)
#                 if response.status_code == requests.codes.ok:
#                     location_instance = Location.objects.get(id=data.get('location'))
#                     client_identifier = data.get('client')
#                     client_instance = Client.objects.get(id=client_identifier) 
#                     if location_instance and client_instance :
#                         accounting_instance = Accounting.objects.create(
#                             client=client_instance,
#                             location=location_instance,
#                             status=True,
#                             error=None,
#                             ort_session_time=0.25,
#                             matting_time=0.25,
#                             main_operation_time=0.25,
#                             image_download_time=0.25
#                         )

#                         output_file_path = os.path.join(ouput_folder, image.name)
#                         with open(output_file_path, 'wb') as out:
#                             out.write(response.content)

#                         temp_file_path = os.path.join(temp_folder, image.name)
#                         with open(temp_file_path, 'wb') as out:
#                             out.write(response.content)
#                         # temp_file_path = x`` out:
#                         #     out.write(response.content)
#                         serializer = AccountingSerializer(accounting_instance)
#                     else:
#                         return build_response(
#                             status.HTTP_400_BAD_REQUEST,
#                             "Location and client are not valid",
#                             data=None,
#                         )
#                 else:
#                     return build_response(
#                         status.HTTP_400_BAD_REQUEST,
#                         f"Failed: {response.status_code} {response.text}",
#                         data=None,
#                     )

#             # Return the final response outside the loop
#             return build_response(
#                 status.HTTP_200_OK,
#                 "Image processed successfully",
#                 data=serializer.data,
#             )
#         else:
#             return build_response(
#                 status.HTTP_400_BAD_REQUEST,
#                 "No image file provided",
#                 data=None,
#             )




class RemoveBackgroundAPIView(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = request.data
    
        location_instance = Location.objects.get(id=data.get('location'))
        client_identifier = data.get('client')
        client_instance = Client.objects.get(id=client_identifier) 
        if location_instance and client_instance :
            accounting_instance = Accounting.objects.create(
                client=client_instance,
                location=location_instance,
                status=True,
                error=None,
                ort_session_time=0.25,
                matting_time=0.25,
                main_operation_time=0.25,
                image_download_time=0.25
            )
 
            serializer = AccountingSerializer(accounting_instance)
    
            return build_response(
                    status.HTTP_200_OK,
                    "Success",
                    data=serializer.data,
                )
        else:
            return build_response(
                status.HTTP_400_BAD_REQUEST,
                f"Failed: {response.status_code} {response.text}",
                data=None,
            )
