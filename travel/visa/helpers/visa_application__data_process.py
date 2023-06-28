from ...models import TravelClient, VBSEmployeeDetails
from django.contrib.auth.models import User
import re

# class manager for TravelVISAApplication
class VisaDataManager:

    morpher_data_store = None
    response = {'status':None, 'message':None}

    def __init__(self, data) -> None:
        self.morpher_data_store = data

    def __convert_client_id_to_object(self):
        try:
            self.morpher_data_store['travel_client_ref'] = TravelClient.objects.get(id=self.morpher_data_store['travel_client_ref'])
        except Exception as e:
            raise Exception('Seems the client selected have conflict through ID. Please verify the client')

    def __passport_validate(self):
        regex = "^[A-PR-WY][1-9]\\d\\s?\\d{4}[1-9]$"
        regmap = re.compile(regex)
        reg_result = re.match(regmap, self.morpher_data_store['passport_no'])

        if reg_result is None:
            return True
        else:
            return False
    

    def __convert_employee_id_to_object(self):
        try:
            self.morpher_data_store['employee_ref'] = VBSEmployeeDetails.objects.get(employee_auth_user_ref=self.morpher_data_store['employee_ref'])
        except Exception as e:
            raise Exception('Seems the employee passed have conflict through ID. Please verify the employee ID')
        
    
    def process_stage1_data(self):
        try:
            self.__convert_client_id_to_object()
            self.__convert_employee_id_to_object()
            if not self.__passport_validate():
                self.response['status'] = 500
                self.response['message'] = 'Passport validation failed. Refer the instructions above.'
                return self.response
            return self.morpher_data_store
        except Exception as e:
            self.response['status'] = 206
            self.response['message'] = 'Seems there is a partial data conflict. Contact developer@vsbizz.com for repair.'
            return self.response
    

    