from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from travel.models import VBSEmployeeDetails

class OrgEmployeeCreation:

    email = ""
    password = ""
    user_group = None
    first_name = None
    last_name = None
    employee_id = None
    new_password = ""

    def __init__(self, **kwargs) -> None:
        self.email = kwargs['email']
        self.password = kwargs['password']
        self.user_group = kwargs['user_group']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.employee_id = kwargs['employee_id']

    def __generate_pbdkf2_code(self):
        try:
            validate_password(self.password)
            self.new_password = make_password(self.password)
            print(self.password)
            print(self.new_password)
            return True
        except Exception as e:
            print(e)
            return False
        
    
    def __generate_username(self):
        print(self.email.split('@')[0])
        return self.email.split('@')[0]

    def add_user_to_db(self):
        if self.__generate_pbdkf2_code():
            try:
                user_obj = User.objects.create_user(email=self.email, username=self.__generate_username(), password=self.password, is_active=True, first_name=self.first_name, last_name = self.last_name)

                VBSEmployeeDetails.objects.create(employee_auth_user_ref=user_obj, org_employee_id=self.employee_id)
                
                user_obj.groups.set([self.__add_to_group()])

                return True

            except Exception as e:
                print(e)
                return False

    def __add_to_group(self):
        group_obj = Group.objects.get(name=self.user_group)
        print(group_obj)
        return group_obj
        
