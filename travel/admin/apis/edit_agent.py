from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from travel.serializers import UserSerializer


class TAdminEditAgent(APIView):

    def put(self, request, id=None):
        data = request.data

        op_status = {'code':status.HTTP_500_INTERNAL_SERVER_ERROR}

        user_obj = User.objects.get(id=int(data.get('id')))


        user_serializer = UserSerializer(user_obj, data=data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            op_status['code'] = status.HTTP_200_OK
            op_status['message'] = 'Successfully edited details.'
        else:
            op_status['message'] = user_serializer.error_messages
            print(user_serializer.error_messages)

        return Response(op_status)
        

