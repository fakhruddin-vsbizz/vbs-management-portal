from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from travel.auth.new_employee_creation import OrgEmployeeCreation

class CreateNewAgentView(APIView):

    def post(self, request, format=None):

        data = request.data

        print(data.get('user_group'))

        try:
            user_obj = User.objects.get(email=data.get('email'))
            return Response({'is_success':False, 'response_message':'User is already present in the system.'})
        except ObjectDoesNotExist as e:
            new_org_employee_creation = OrgEmployeeCreation(email=data.get('email'), password=data.get('password'), user_group = data.get('user_group'), first_name = data.get('first_name'), last_name = data.get('last_name'), employee_id=data.get('employee_id')).add_user_to_db()
            
            if new_org_employee_creation:
                return Response({'is_success':True, 'response_message':'User created successfully'})
            else:
                return Response({'is_success':False, 'response_message':'Some issue occured while creating the employee account. Please contact developer@vsbizz.com'})
            

