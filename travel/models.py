from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
import datetime

class VBSEmployeeDetails(models.Model):
    employee_auth_user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    org_employee_id = models.CharField(max_length=50, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = 'vbs_employee_details'

class TravelClient(models.Model):
    admin_auth_user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=200, null=False, blank=False, default="")
    organization = models.CharField(max_length=200, null=False, blank=False, default="")
    contact_number = models.CharField(max_length=200, null=False, blank=False, default="")
    email = models.EmailField(blank=False, null=False)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        db_table = 'vbs_travel_client'

    def save(self, *args, **kwargs):
        travel_client_obj = TravelClient.objects.filter(client_name=self.client_name, contact_number=self.contact_number)
        if len(travel_client_obj) == 0:
            super(TravelClient, self).save(*args, **kwargs)
        elif len(travel_client_obj) > 0:
            raise Exception("Client is already present. Please keep a different contact number and name combination")

class TravelPackagesApplication(models.Model):
    employee_ref = models.ForeignKey(VBSEmployeeDetails, on_delete=models.CASCADE)
    travel_client_ref = models.ForeignKey(TravelClient, on_delete=models.CASCADE)
    applicants_name = models.CharField(max_length=200, null=False, blank=False, default="")
    stage = models.CharField(max_length=200, null=False, blank=False, default="")
    status = models.CharField(max_length=200, null=False, blank=False, default="open")
    vendor_name = models.CharField(max_length=200, null=False, blank=False, default="")
    total_vendor_payment = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    first_installment = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    second_installment = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    third_installment = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    less_taxes = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=False, blank=False) # type: ignore
    no_of_days = models.IntegerField(default=0, null=False, blank=False)
    passport_no = models.CharField(max_length=200, null=False, blank=False, default="")
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    service_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    invoice_status = models.BooleanField(max_length=10, blank=False, null=False, default=False)
    tentative_payment_date = models.DateTimeField(blank=True, null=True, default="")# type: ignore
    arrival_date = models.DateTimeField(blank=True, null=True, default="") # type: ignore
    departure_date = models.DateTimeField(blank=True, null=True, default="")# type: ignore
    destination = models.CharField(max_length=200, null=False, blank=False, default="")
    boarding = models.CharField(max_length=200, null=False, blank=False, default="")
    package_type = models.CharField(max_length=200, null=False, blank=False, default="")
    quantity_of_packages = models.CharField(max_length=200, null=False, blank=False, default="")
    package_name = models.CharField(max_length=200, null=False, blank=False, default="")
    created_on = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        db_table = 'travel_packages_application'

class TravelTicketsApplication(models.Model):
    employee_ref = models.ForeignKey(VBSEmployeeDetails, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=200, null=False, blank=False, default="")
    client_name = models.CharField(max_length=200, null=False, blank=False, default="")
    applicants_name = models.CharField(max_length=200, null=False, blank=False, default="")
    stage = models.CharField(max_length=200, null=False, blank=False, default="")
    status = models.CharField(max_length=200, null=False, blank=False, default="open")
    contact_number = models.CharField(max_length=200, null=False, blank=False, default="")
    trip_type = models.CharField(max_length=200, null=False, blank=False, default="")
    created_on = models.DateTimeField(default=datetime.datetime.now)
    invoice_status = models.BooleanField(max_length=10, blank=False, null=False, default=False)
    travel_client_ref = models.ForeignKey(TravelClient, on_delete=models.CASCADE)
    origin = models.CharField(max_length=200, null=False, blank=False, default="")
    destination = models.CharField(max_length=200, null=False, blank=False, default="")
    via = models.CharField(max_length=200, null=False, blank=False, default="")
    mode_of_transport = models.CharField(max_length=200, null=False, blank=False, default="")
    vehicle_no = models.CharField(max_length=200, null=False, blank=False, default="")
    travel_class = models.CharField(max_length=200, null=False, blank=False, default="")
    gds_pnr_no = models.CharField(max_length=200, null=False, blank=False, default="")
    airline_pnr_no = models.CharField(max_length=200, null=False, blank=False, default="")
    departure_date = models.DateTimeField(blank=True)
    arrival_date = models.DateTimeField(blank=True)
    base_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    service_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    markup = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    issued_from = models.CharField(max_length=200, null=False, blank=False, default="")

    class Meta:
        db_table = 'travel_tickets_application'


class TravelPackagesVendorPayment(models.Model):
    package_appl_id = models.ForeignKey(TravelPackagesApplication, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    vendor_name = models.CharField(max_length=200, null=False, blank=False, default="")# type: ignore
    vendor_payment_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    vendor_payment_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    vendor_payment_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    less_taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)# type: ignore
    created_on = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        db_table = 'travel_packages_vendor_payment'

class TravelApplicationControlTransfer(models.Model):
    previous_agent_id = models.ForeignKey(VBSEmployeeDetails, on_delete=models.CASCADE)
    # new_agent_id = models.ForeignKey(VBSEmployeeDetails, on_delete=models.CASCADE)
    new_agent_id = models.CharField(max_length=200, null=False, blank=False, default="")
    appl_id = models.CharField(max_length=200, null=False, blank=False, default="")
    is_transfer_revoked = models.BooleanField(max_length=10, blank=False, null=False, default=False)
    created_on = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'travel_appl_control_transfer'

class FollowUps(models.Model):
    employee_id = models.ForeignKey(VBSEmployeeDetails, on_delete=models.CASCADE)
    appl_id = models.CharField(max_length=200, null=False, blank=False, default="")
    application_type = models.CharField(max_length=200, null=False, blank=False, default="")
    followup_stage = models.CharField(max_length=200, null=False, blank=False, default="")
    time_for_followups = models.DateTimeField(default=datetime.datetime.now)
    created_on = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'followups'

class TravelVisaApplication(models.Model):
    employee_ref = models.ForeignKey(VBSEmployeeDetails, on_delete=models.CASCADE)
    travel_client_ref = models.ForeignKey(TravelClient, on_delete=models.CASCADE)
    applicants_name = models.CharField(max_length=200, null=False, blank=False, default="")
    passport_no = models.CharField(max_length=200, null=False, blank=False, default="")
    contact_number = models.CharField(max_length=200, null=False, blank=False, default="")
    visiting_country = models.CharField(max_length=200, null=False, blank=False, default="")
    stage = models.CharField(max_length=200, null=False, blank=False, default="detail processing")
    status = models.CharField(max_length=200, null=False, blank=False, default="pending")
    invoice_status = models.BooleanField(blank=False, null=False, default=False)
    total_charges = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0, null=False, blank=False)# type: ignore
    cgst_fees = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0, null=False, blank=False)# type: ignore
    sgst_fees = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0, null=False, blank=False)# type: ignore
    vbs_charges = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0, null=False, blank=False)# type: ignore
    express_charges = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0, null=False, blank=False)# type: ignore
    authority_fee = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0, null=False, blank=False)# type: ignore
    visa_fee = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0, null=False, blank=False)# type: ignore
    vendor_name = models.CharField(max_length=200, null=False, blank=False, default="")
    sub_location = models.CharField(max_length=200, null=False, blank=False, default="")
    handover_date = models.DateTimeField(blank=True, null=True)
    courier_in_date = models.DateTimeField(blank=True, null=True)
    courier_out_date = models.DateTimeField(blank=True, null=True)
    document_collection_date = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        db_table = 'travel_visa_application'
