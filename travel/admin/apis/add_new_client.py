from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from ..helpers.travel_admin__new_client import TAdminNewClientHelper


class TAdminCreateClient(APIView):

    def post(self, request, format=None):

        data = request.data.copy()

        data['admin_user'] = request.user
        

        # status code handles
        response_body = {'status':status.HTTP_200_OK, 'message':'Client created successfully'}

        try:
            travel_new_client_manager = TAdminNewClientHelper(**data)
            op_status = travel_new_client_manager.createClient()
            print(op_status['message'])
        except Exception as e:
            response_body['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_body['message'] = str(e)
            print(response_body)

        return Response(response_body)