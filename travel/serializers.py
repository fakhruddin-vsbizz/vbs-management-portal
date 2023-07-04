from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import  (
    TravelVisaApplication, TravelPackagesApplication, TravelTicketsApplication,  TravelClient, VBSEmployeeDetails,
    TravelPackagesApplication,
    TravelTicketsApplication
)


class UserSerializer(ModelSerializer):
    class Meta:
        model= User
        fields='__all__'

class VBSEmployeeDetailsSerializer(ModelSerializer):
    employee_auth_user_ref=UserSerializer()
    class Meta:
        model= VBSEmployeeDetails
        fields='__all__'
        
class TravelClientSerializer(ModelSerializer):
    class Meta:
        model= TravelClient
        fields='__all__'

class TravelVisaApplicationSerializer(ModelSerializer):
    employee_ref = VBSEmployeeDetailsSerializer()
    travel_client_ref=TravelClientSerializer()
    class Meta:
        model = TravelVisaApplication
        fields='__all__'