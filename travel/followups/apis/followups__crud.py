from rest_framework.response import Response
from rest_framework import status
from ...models import VBSEmployeeDetails, TravelFollowUps, TravelVisaApplication, TravelPackagesApplication, TravelTicketsApplication
from ...serializers import TravelFollowUpSerializer
from rest_framework.views import APIView

import datetime



class TravelFollowupAPI(APIView):

    def __return_vbs_employee_id(self, employee_id):
        return VBSEmployeeDetails.objects.get(employee_auth_user_ref=employee_id).id

    
    def post(self, request, format=None):

        response_msg = {'status':status.HTTP_204_NO_CONTENT, 'message':'No content available'}
        data = request.data.copy()

        data['employee_id'] = self.__return_vbs_employee_id(request.data.get('employee_id'))

        if data.get('appl_id') == '':
            response_msg['message'] = 'New applications cant create followups. Create application and then create followups.'
            response_msg['status'] = status.HTTP_306_RESERVED
        else:
            travel_followup_serializer =  TravelFollowUpSerializer(data=data)
            try:
                if travel_followup_serializer.is_valid():
                    travel_followup_serializer.save()
                    response_msg['status'] = status.HTTP_200_OK
                    response_msg['message'] = 'Follow-up created successfully'

                    match data.get('application_type'):

                        case 'visa':
                            TravelVisaApplication.objects.filter(id=data.get('appl_id')).update(status='blocked')

                        case 'packages':
                            TravelPackagesApplication.objects.filter(id=data.get('appl_id')).update(status='blocked')

                        case 'tickets':
                            TravelTicketsApplication.objects.filter(id=data.get('appl_id')).update(status='blocked')

                        case _:
                            pass

                else:
                    print(travel_followup_serializer.errors)
                    response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                    response_msg['message'] = 'Some validation issues have occured.'
            except Exception as e:
                response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_msg['message'] = 'Some server side issue occured. Try again.'
        

        return Response(response_msg)
    
    def put(self, request, id=None):

        data = request.data.copy()

        print(data.get('id'))

        try:
            travel_followup_obj = TravelFollowUps.objects.get(id=data.get('id'))
            travel_followup_serializer = TravelFollowUpSerializer(travel_followup_obj, data=data, partial=True)

            if travel_followup_serializer.is_valid():
                travel_followup_serializer.save()
            else:
                print(travel_followup_serializer.errors)
        except Exception as e:
            print(e)

        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'No content'})