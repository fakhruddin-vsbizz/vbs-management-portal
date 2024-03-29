from rest_framework.views import APIView
from ...models import TravelVisaApplication
from rest_framework.response import Response
from rest_framework import status
from ...serializers import TravelVisaApplicationSerializer
from ..helpers.visa_application__data_process import VisaDataManager
from django.http.request import QueryDict
import datetime
import pytz

class TravelApplicationInitiateAPIView(APIView):

    # localize the dates
    def __return_datetime_object(self, stringified_date):
        return datetime.datetime.strptime(stringified_date.replace(" GMT+0530 (India Standard Time)",""), '%a %b %d %Y %H:%M:%S') if stringified_date != '' else None


    # POST request to initiate new visa application 
    def post(self, request, format=None):
        data = request.data.copy()
        response_msg = {'status': status.HTTP_204_NO_CONTENT, 'message':'In Progress'}
        visa_manager = VisaDataManager(data)

        try:
            print('here we go 1')
            response_store = visa_manager.process_stage1_data()
            if response_store['csrfmiddlewaretoken']:# type: ignore
                response_store = dict(response_store) # type: ignore
                response_store.pop('csrfmiddlewaretoken')# type: ignore
                print('here we go 2')

                response_store['id'] = TravelVisaApplication.objects.count()+1 if data.get('id') == '0' else data.get('id')# type: ignore


                print('here we go 3')

                print(response_store)

                for key, value in response_store.items():
                    try:
                        response_store[key] = value[0]# type: ignore
                    except Exception as e:
                        response_store[key] = value

                TravelVisaApplication.objects.update_or_create(
                    id=TravelVisaApplication.objects.count()+1 if not data.get('id') else data.get('id'),
                    defaults=response_store# type: ignore
                )

            response_msg['status'] = status.HTTP_200_OK
            response_msg['message'] = 'Saved the details successfully'
            response_msg['id'] = TravelVisaApplication.objects.count()



        except Exception as e:
                print(e)
                response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_msg['message'] = str(e)
        return Response(response_msg)


    # PUT request to update application details
    def put(self, request, id=None):
        data = request.data.copy()
        response_msg = {'status': status.HTTP_204_NO_CONTENT, 'message':'In Progress'}
        travel_visa_appl = TravelVisaApplication.objects.get(id=data.get('app_id'))

        print(data)
        
        if data.get('stage') == 'processing documents':
            if(data.get('document_collection_date')):
                data['document_collection_date'] = self.__return_datetime_object(data['document_collection_date'])
            
            if(data.get('submission_date')):
                data['submission_date'] = self.__return_datetime_object(data['submission_date'])
            
            if(data.get('courier_out_date')):
                data['courier_out_date'] = self.__return_datetime_object(data['courier_out_date'])

            if(data.get('courier_in_date')):
                data['courier_in_date'] = self.__return_datetime_object(data['courier_in_date'])

            if(data.get('handover_date')):
                data['handover_date'] = self.__return_datetime_object(data['handover_date'])
                
            if 'new_stage' in data:
                if(data.get('new_stage')):
                    data['stage'] = "processing payments"
                    data.pop('new_stage')

        try:
            travel_visa_serializer = TravelVisaApplicationSerializer(travel_visa_appl, data=data, partial=True)

            if travel_visa_serializer.is_valid():
                print("IT IS VALID")
                travel_visa_serializer.save()
                response_msg['status'] = status.HTTP_200_OK
                response_msg['message'] = "Successfully saved details"
                response_msg['id'] = data.get('app_id')
            else:
                print(travel_visa_serializer.errors)
                response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_msg['message'] = travel_visa_serializer.errors
            
        except Exception as e:
             response_msg['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
             response_msg['message'] = str(e)

        return Response(response_msg)
