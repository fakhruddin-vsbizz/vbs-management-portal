from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import TravelVisaApplication


class UserSerializer(ModelSerializer):
    class Meta:
        model= User
        fields='__all__'


class TravelVisaApplicationSerializer(ModelSerializer):
    class Meta:
        model = TravelVisaApplication
        fields='__all__'