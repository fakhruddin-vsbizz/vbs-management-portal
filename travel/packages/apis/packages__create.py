from ...models import TravelPackagesApplication
from ...serializers import TravelPackagesApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import TravelClient, VBSEmployeeDetails

from django.contrib.auth.models import User


import datetime


class TravelPackagesActionHandlerAPI(APIView):

    def __return_datetime(self, date_time_string):
        return datetime.datetime.strptime(date_time_string.replace(" GMT+0530 (India Standard Time)",".000000"), '%a %b %d %Y %H:%M:%S.%f') if date_time_string is not '' else None

    def __travel_client_reference_binder(self, travel_client_id):
        return TravelClient.objects.get(id=int(travel_client_id))
        
    def __employee_reference_binder(self, employee_id):
        return VBSEmployeeDetails.objects.get(employee_auth_user_ref=int(employee_id))

    def post(self, request, format=None):

        data = request.data.copy()
        response_msg = {'status_code': status.HTTP_204_NO_CONTENT, 'message':None}

        main_app_id = None
        data.pop('csrfmiddlewaretoken')

        print(data)

        data['travel_client_ref'] = self.__travel_client_reference_binder(data.get('travel_client_ref'))
        data['employee_ref'] = self.__employee_reference_binder(data.get('employee_ref'))
        data['arrival_date'] = self.__return_datetime(request.data.get('arrival_date'))
        data['departure_date'] = self.__return_datetime(request.data.get('departure_date'))

        if request.data.get('id') == '':
            data.pop('id')
            main_app_id = TravelPackagesApplication.objects.count()+1
        else:
            main_app_id = request.data.get('id')


        data = dict(data)

        for key, value in data.items():
            try:
                data[key] = value[0]
            except Exception as e:
                data[key] = value

        try:
            travel_package_obj =  TravelPackagesApplication.objects.update_or_create(
                id=main_app_id,
                defaults=data
            )

            response_msg['status_code'] = status.HTTP_200_OK
            response_msg['message'] = 'Saved details successfully.'
            response_msg['id'] = travel_package_obj[0].id

        except Exception as e:
            print(e)
            response_msg['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_msg['message'] = str(e)

        return Response(response_msg)
    
    def put(self, request, id=None):

        data = request.data.copy()
        
        response_msg = {'status': status.HTTP_204_NO_CONTENT, 'message':'In Progress'}
        travel_packages_obj = TravelPackagesApplication.objects.get(id=data.get('app_id'))

        try:

            if data.get('stage') == 'customer_invoicing' and 'tentative_payment_date' in data:
                data['tentative_payment_date'] = self.__return_datetime(data.get('tentative_payment_date'))
                
            if 'stage_changes' in data:
                data['stage'] = data['stage_changes']
                data.pop('stage_changes')

            travel_packages_serializer = TravelPackagesApplicationSerializer(travel_packages_obj, data=data, partial=True)

            if travel_packages_serializer.is_valid():
                travel_packages_serializer.save()
                response_msg['status'] = status.HTTP_200_OK
                response_msg['message'] = 'Saved details successfully.'
                response_msg['id'] = data.get('app_id')
            else:
                print(travel_packages_serializer.errors)
                response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_msg['message'] = 'Some vaidation issues have occured'
        except Exception as e:
            response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_msg['message'] = str(e)

        return Response(response_msg)