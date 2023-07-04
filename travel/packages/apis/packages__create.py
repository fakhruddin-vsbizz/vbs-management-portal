from ...models import TravelPackagesApplication
from ...serializers import TravelPackagesApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import TravelClient, VBSEmployeeDetails

from django.contrib.auth.models import User

import datetime
from datetime import timezone


class TravelPackagesActionHandlerAPI(APIView):

    def __return_datetime(self, date_time_string):
        print(date_time_string)
        return datetime.datetime.strptime(date_time_string+" 00:00:00", "%Y-%m-%d %H:%M:%S")
    
    def __travel_client_reference_binder(self, travel_client_id):
        return int(travel_client_id)
        
    def __employee_reference_binder(self, employee_id):
        return VBSEmployeeDetails.objects.get(employee_auth_user_ref=int(employee_id)).id

    def post(self, request, format=None):

        data = request.data.copy()

        date_list = request.POST['arrival_date'].split('-')

        formated_date = datetime.date(int(date_list[0]),int(date_list[1]),int(date_list[2]))

        print("formated_date ============== ",formated_date)

        data['travel_client_ref'] = self.__travel_client_reference_binder(data.get('travel_client_ref'))
        data['employee_ref'] = self.__employee_reference_binder(data.get('employee_ref'))
        data['arrival_date'] = "2012-09-04 06:00:00.000000-08:00"
        data['departure_date'] = "2012-09-04 06:00:00.000000-08:00"

        print("=====================")
        print(data)

        if data.get('id') == '':
            data.pop('id')

        travel_package_serializer = TravelPackagesApplicationSerializer(data=data)
        if travel_package_serializer.is_valid():
            print('VALID HAI')
            travel_package_serializer.save()
        else:
            print('INVALID HAI')
            print(travel_package_serializer.errors)
        return Response({'status_code': status.HTTP_204_NO_CONTENT})
    
    def put(self, request, id=None):
        return Response({'status_code': status.HTTP_204_NO_CONTENT})