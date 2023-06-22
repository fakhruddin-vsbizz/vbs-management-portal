from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

class TAdminCreateClient(APIView):

    def post(self, request, format=None):
        
        return Response({'status':'IN DEVELOPMENT', 'is_complete': False})