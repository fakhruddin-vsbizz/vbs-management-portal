from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User

class VBSEmployeeDetails(models.Model):
    employee_auth_user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    org_employee_id = models.CharField(max_length=50, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'vbs_employee_details'

class TravelClient(models.Model):
    admin_auth_user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=200, null=False, blank=False)
    organization = models.CharField(max_length=200, null=False, blank=False)
    contact_number = models.IntegerField(max_length=10, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vbs_travel_client'

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        travel_client_obj = TravelClient.objects.filter(client_name=self.client_name, contact_number=self.contact_number)
        if len(travel_client_obj) == 0:
            super().save(force_insert, force_update, using, update_fields)
        elif len(travel_client_obj) > 0:
            raise Exception("Client is already present. Please keep a different contact number and name combination")

