from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

class OrgAuth:

    # class variables to manage auth ops 
    __request = None
    email = None
    password = None
    __user_obj = None

    
    # loading constructor with request, email and password of auth form
    def __init__(self, request, email, password) -> None:
        self.__request = request
        self.email = email
        self.password = password
    
    # [private] returns username referencing email passed
    # IMP: DO NOT MAKE THIS FUNCTION PUBLIC. Use request.user if needed.
    def __get_username(self):
        try:
            print(self.email)
            self.__user_obj = User.objects.get(email=self.email)
            return True
        except Exception as e:
            return False
        
    # returns boolean if user is authenticated or not
    # [NEWSOL] return type will be object to pass a custom message to be set as response
    def return_if_is_authenticated(self):
        if(self.__get_username()):
            self.__user_obj = authenticate(username=self.__user_obj.username, password=self.password)
            if self.__user_obj is not None:
                login(self.__request, self.__user_obj)
                return True
            else:
                return False

    # returns group type for the authenticated user only
    # IMP: DO NOT MAKE THIS FUNCTION PUBLIC. Use role_redirect() if needed.
    def __return_auth_group(self):
        user_groups = self.__user_obj.groups.all().values_list('name', flat=True)
        return list(user_groups)
    
    
    # returns path for redirecting the user to its designated dashboard
    # IMP: Do not use the code below 3.10.0 since match support is >3.10.0
    def role_redirect(self):
        try:
            match self.__return_auth_group()[0]:
                case "travel_admin":
                    return 'travel/admin/agents.html'
                case "travel_agent":
                    return 'travel/visa/all_list.html'
                case _:
                    return 'travel/auth/login.html'
        except Exception as e:
            return 'travel/auth/login.html'
