from django.db import models
from django.contrib.auth.models import User

class VBSEmployeeDetails(models.Model):
    employee_auth_user_ref = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    org_employee_id = models.CharField(max_length=50, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'vbs_employee_details'

# Manage 