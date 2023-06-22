from travel.models import TravelClient

class TAdminNewClientHelper:
    __admin_user_obj = None
    first_name = None
    last_name = None
    organization = None
    contact_number = None
    email = None
    
    def __init__(self, **kwargs) -> None:
        for key, values in kwargs.items():
            kwargs[key] = values[0]

            
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.organization = kwargs['organization']
        self.contact_number = kwargs['contact_number']
        self.email = kwargs['email']
        self.__admin_user_obj = kwargs['admin_user']

        

    
    
    def createClient(self):

        status = {'is_created':None, 'message':None}

        try:
            TravelClient.objects.create(
                admin_auth_user_ref = self.__admin_user_obj,
                client_name = self.first_name+' '+self.last_name,
                organization = self.organization,
                contact_number = self.contact_number,
                email = self.email
            )

            status['is_created'] = True
            status['message'] = 'Client has been created successfully'

        except Exception as e:
            status['is_created'] = False
            status['message'] = str(e)
        
        return status

