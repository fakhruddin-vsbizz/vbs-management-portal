from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import  TravelVisaApplication, TravelPackagesApplication, TravelTicketsApplication,  TravelClient, VBSEmployeeDetails, FollowUps


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
        
class TravelTicketsApplicationSerializer(ModelSerializer):
    employee_ref = VBSEmployeeDetailsSerializer()
    travel_client_ref=TravelClientSerializer()
    class Meta:
        model = TravelTicketsApplication
        fields='__all__'
        
class TravelPackagesApplicationSerializer(ModelSerializer):
    employee_ref = VBSEmployeeDetailsSerializer()
    travel_client_ref=TravelClientSerializer()
    class Meta:
        model = TravelPackagesApplication
        fields='__all__'

class FollowUpSerializer(ModelSerializer):
    class Meta:
        model = FollowUps
        fields = '__all__'
