from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from travel.serializers import TravelFollowUpSerializer

from travel.models import TravelFollowUps, VBSEmployeeDetails

class TFollowUpCreate(APIView):
    
    # def get(self, request):
        
    #     print(request)
    #     # follow_up = TravelFollowUps.objects.get(appl_id=request.data.get('app_id'))
    #     # serialize = TravelFollowUpSerializer(follow_up, many=True)
        
    #     content = {
    #         'status': 1, 
    #         'responseCode' : status.HTTP_200_OK, 
    #         'data': [],
    #     }
        
    #     return JsonResponse(content)

    def post(self, request, format=None):

        data = request.data.copy()

        print(data)
        
        try:
            exists = TravelFollowUps.objects.get(appl_id=data['appl_id'], application_type=data['application_type'])
        except TravelFollowUps.DoesNotExist:
            exists = None
        
        # exists = TravelFollowUps.objects.get(appl_id=2, application_type=data['application_type'])
        
        response_body = {'status':status.HTTP_200_OK, 'message':'Client created successfully'}
        
        data['employee'] = VBSEmployeeDetails.objects.get(id=data.get('employee_id'))
        
        print('line 43')
        print(exists)
        
        if exists is not None:
            print('line 47')
            
            try:
                follow_up_serializer = TravelFollowUpSerializer(exists, data=data, partial=True)
                print('line 51')
                

                if follow_up_serializer.is_valid():
                    print('line 55')
                    
                    print("IT IS VALID")
                    follow_up_serializer.save()
                    response_body['status'] = status.HTTP_200_OK
                    response_body['message'] = "Successfully saved details"
                    response_body['id'] = data.get('app_id')
                else:
                    print('line 63')
                    
                    print(follow_up_serializer.errors)
                    response_body['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                    response_body['message'] = follow_up_serializer.errors
            
            except Exception as e:
                response_body['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_body['message'] = str(e)
        else:
            try:
                TravelFollowUps.objects.create(
                    employee_id = data['employee'],
                    appl_id = data['appl_id'],
                    name = data['name'],
                    contact_number = data['contact_number'],
                    application_type = data['application_type'],
                    followup_stage = data['followup_stage'],
                    time_for_followups = data['time_for_followups'],
                    date_for_followups = data['date_for_followups'],
                    remarks = data['remarks']
                )
                # print(op_status['message'])
            except Exception as e:
                response_body['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_body['message'] = str(e)
                print(response_body)
        

        return Response(response_body)
    
    def put(self, request, id=None):
        data = request.data.copy()
        response_msg = {'status': status.HTTP_204_NO_CONTENT, 'message':'In Progress'}
        
        try:
            follow_up = TravelFollowUps.objects.get(appl_id=data.get('id'), application_type=data['application_type'])
        except TravelFollowUps.DoesNotExist:
            follow_up = None

        if follow_up is not None:
            try:
                follow_up_serializer = TravelFollowUpSerializer(follow_up, data=data, partial=True)

                if follow_up_serializer.is_valid():
                    print("IT IS VALID")
                    follow_up_serializer.save()
                    response_msg['status'] = status.HTTP_200_OK
                    response_msg['message'] = "Successfully saved details"
                    response_msg['id'] = data.get('app_id')
                else:
                    print(follow_up_serializer.errors)
                    response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                    response_msg['message'] = follow_up_serializer.errors
                
            except Exception as e:
                response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_msg['message'] = str(e)
        else:
            response_msg['status'] = status.HTTP_404_NOT_FOUND
            response_msg['message'] = "Does not exist"

        return Response(response_msg)
