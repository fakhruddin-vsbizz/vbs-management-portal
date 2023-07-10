from rest_framework.response import Response
from rest_framework import status
from ...models import TravelTicketsApplication, TravelClient, VBSEmployeeDetails
from ...serializers import TravelTicketsApplicationSerializer
from rest_framework.views import APIView

import datetime



class TravelTicketsActionHandlerAPI(APIView):

    def __return_datetime(self, date_time_string):
        return datetime.datetime.strptime(date_time_string.replace(" GMT+0530 (India Standard Time)",".000000"), '%a %b %d %Y %H:%M:%S.%f') if date_time_string is not '' else None

    def __travel_client_reference_binder(self, travel_client_id):
        return TravelClient.objects.get(id=int(travel_client_id)).id
        
    def __employee_reference_binder(self, employee_id):
        return VBSEmployeeDetails.objects.get(employee_auth_user_ref=int(employee_id)).id

    def post(self, request, format=None):

        data = request.data.copy()
        response_msg = {'status':status.HTTP_204_NO_CONTENT, 'message':'No content available'}

        if request.data.get('stage') == 'customer_details':
            data['employee_ref'] = self.__employee_reference_binder(request.data.get('employee_ref'))
            data['travel_client_ref'] = self.__travel_client_reference_binder(request.data.get('travel_client_ref'))

        if request.data.get('stage') == 'transport_details':
            data['departure_date'] = self.__return_datetime(request.data.get('departure_date'))
            data['arrival_date'] = self.__return_datetime(request.data.get('arrival_date'))

        print(data)
        
        try:

            travel_tickets_serializer = None

            if request.data.get('app_id'):

                travel_tickets_obj = TravelTicketsApplication.objects.get(id=int(request.data.get('app_id')))

                travel_tickets_serializer = TravelTicketsApplicationSerializer(travel_tickets_obj, data=data, partial=True) 

            else:
                   travel_tickets_serializer = TravelTicketsApplicationSerializer( data=data) 
            
            
            if travel_tickets_serializer.is_valid():
                print('saving')
                travel_tickets_serializer.save()
                print('saved')
                response_msg['status'] = status.HTTP_200_OK
                response_msg['message'] = 'Saved details successfully'
                response_msg['id'] = travel_tickets_serializer.data['id']
            else:
                response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_msg['message'] = str(travel_tickets_serializer.errors)
                print(travel_tickets_serializer.errors)
        except Exception as e:
            response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_msg['message'] = str(e)
            print(e)

        return Response(response_msg)
    
    def put(self, request, id=None):
        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'No content available'})