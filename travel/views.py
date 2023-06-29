from typing import Any, Dict
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from travel.auth.login import OrgAuth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .variables import COUNTRIES
import datetime
from .models import TravelClient, VBSEmployeeDetails, TravelVisaApplication, TravelPackagesApplication, TravelTicketsApplication

# Create your views here.

def LoginView(request):
    
    is_validated = None
    role = None

    if request.method == 'POST':

        # getting if user authenticated or not
        org_auth_obj = OrgAuth(request, request.POST.get('email'), request.POST.get('password'))

        # sets the message if user is valid
        is_validated = org_auth_obj.return_if_is_authenticated()
        
        role = org_auth_obj.role_redirect()
        
        if is_validated is False:
            return render(request, "travel/auth/login.html", {'auth_validated':is_validated})
            # return redirect(role)

        # returns the admin/employee for travel/recruitment
        if(role is not None and is_validated is not False):
            return redirect(role)
    else:
        return render(request, "travel/auth/login.html", {'auth_validated':is_validated})

def logout_view(request):
    logout(request)
    return redirect("/travel/auth/login")


# TRAVEL VISA VIEWS
class TravelVISA(TemplateView):
    
    def get(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        filter_visa_data = TravelVisaApplication.objects.filter(employee_ref=id)
        visa_data = TravelVisaApplication.objects.filter(employee_ref=id).order_by("handover_date")
        return render(request, 'travel/visa/all_list.html', {"visa_data": visa_data, "filter_visa_data": filter_visa_data})
    
    def post(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        applicants_name = request.POST['applicants_name']
        client_name = request.POST['client_name']
        stage = request.POST['stage']
        status = request.POST['status']
        created_on = request.POST['created_on'] 
        handover_date = request.POST['handover_date'] 
        
        if applicants_name != "" and client_name != "" and status != "select" and stage != "select stage" and created_on != "" and handover_date != "":
            created_on_List = created_on.split("-")      
            cx = datetime.date(int(created_on_List[0]), int(created_on_List[1]), int(created_on_List[2]))
            handover_date_List = handover_date.split("-")      
            hx = datetime.date(int(handover_date_List[0]), int(handover_date_List[1]), int(handover_date_List[2])) 
            filter_visa_data_by_id = TravelVisaApplication.objects.filter(employee_ref=id, applicants_name=applicants_name, stage=stage, status=status)
            filter_visa_data = [i for i in filter_visa_data_by_id if i.travel_client_ref.client_name == client_name and i.created_on.date() == cx and i.handover_date.date() == hx]
        elif applicants_name != "" and client_name != "" and status != "select" and stage != "select stage":
            filter_visa_data_by_id = TravelVisaApplication.objects.filter(employee_ref=id, applicants_name=applicants_name, stage=stage, status=status)
            filter_visa_data = [i for i in filter_visa_data_by_id if i.travel_client_ref.client_name == client_name]
        elif applicants_name != "" and client_name != "":
            filter_visa_data_by_id = TravelVisaApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
            filter_visa_data = [i for i in filter_visa_data_by_id if i.travel_client_ref.client_name == client_name]
        # elif applicants_name != "" and client_name != "":
        #     filter_visa_data_by_id = TravelVisaApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
        #     filter_visa_data = [i for i in filter_visa_data_by_id if i.travel_client_ref.client_name == client_name]
        elif applicants_name != "":
            filter_visa_data = TravelVisaApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
        elif created_on != "":
            created_on_List = created_on.split("-")      
            x = datetime.date(int(created_on_List[0]), int(created_on_List[1]), int(created_on_List[2])) 
            filter_visa_data_by_id = TravelVisaApplication.objects.filter(employee_ref=id)
            filter_visa_data = [i for i in filter_visa_data_by_id if i.created_on.date() == x]
        elif handover_date != "":
            handover_date_List = handover_date.split("-")      
            x = datetime.date(int(handover_date_List[0]), int(handover_date_List[1]), int(handover_date_List[2])) 
            filter_visa_data_by_id = TravelVisaApplication.objects.filter(employee_ref=id)
            filter_visa_data = [i for i in filter_visa_data_by_id if i.handover_date.date() == x]
        elif status != "select":
            filter_visa_data = TravelVisaApplication.objects.filter(employee_ref=id, status=status)
        elif stage != "select stage":
            filter_visa_data = TravelVisaApplication.objects.filter(employee_ref=id, stage=stage)
        elif client_name != "":
            filter_visa_data_by_id = TravelVisaApplication.objects.filter(employee_ref=id)
            filter_visa_data = [i for i in filter_visa_data_by_id if i.travel_client_ref.client_name == client_name]
        else:
            filter_visa_data = TravelVisaApplication.objects.filter(employee_ref=id)
        
        visa_data = TravelVisaApplication.objects.filter(employee_ref=id).order_by("handover_date")
        return render(request, 'travel/visa/all_list.html', {"visa_data": visa_data, "filter_visa_data": filter_visa_data})
    



class TVDetailProcessing(TemplateView):

    template_name = "travel/visa/detail_processing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        updated_context = super().get_context_data(**kwargs)
        updated_context['all_travel_clients'] = TravelClient.objects.all()
        updated_context['countries'] = COUNTRIES
        return updated_context
    

class TVDocumentProcessing(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'travel/visa/document_processing.html', {'app_id':kwargs['app_pk']})


class TVPaymentProcessing(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'travel/visa/payment_processing.html', {'app_id':kwargs['app_pk']})


# TRAVEL PACKAGE
class TPPackageSelection(TemplateView):

    template_name = "travel/packages/package_selection.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)
    

class TPCustomerInvoicing(TemplateView):

    template_name = "travel/packages/customer_invoicing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)
    
class TPVendorPayments(TemplateView):

    template_name = "travel/packages/vendor_management.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


class TravelPackages(TemplateView):

    def get(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        filter_package_data = TravelPackagesApplication.objects.filter(employee_ref=id)
        package_data = TravelPackagesApplication.objects.filter(employee_ref=id).order_by("departure_date")
        return render(request, "travel/packages/all_list.html", {"package_data": package_data, "filter_package_data": filter_package_data})
    
    def post(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        applicants_name = request.POST['applicants_name']
        client_name = request.POST['client_name']
        stage = request.POST['stage']
        status = request.POST['status']
        created_on = request.POST['created_on']
        tentative_payment_date = request.POST['tentative_payment_date'] 
        
        if applicants_name != "" and client_name != "" and status != "select" and stage != "select stage" and created_on != "" and tentative_payment_date != "":
            created_on_List = created_on.split("-")      
            cx = datetime.date(int(created_on_List[0]), int(created_on_List[1]), int(created_on_List[2]))
            tentative_payment_date_List = tentative_payment_date.split("-")      
            tx = datetime.date(int(tentative_payment_date_List[0]), int(tentative_payment_date_List[1]), int(tentative_payment_date_List[2])) 
            filter_package_data_by_id = TravelPackagesApplication.objects.filter(employee_ref=id, applicants_name=applicants_name, stage=stage, status=status)
            filter_package_data = [i for i in filter_package_data_by_id if i.travel_client_ref.client_name == client_name and i.created_on.date() == cx and i.tentative_payment_date.date() == tx]
        elif applicants_name != "" and client_name != "" and status != "select" and stage != "select stage":
            filter_package_data_by_id = TravelPackagesApplication.objects.filter(employee_ref=id, applicants_name=applicants_name, stage=stage, status=status)
            filter_package_data = [i for i in filter_package_data_by_id if i.travel_client_ref.client_name == client_name]
        # elif applicants_name != "" and client_name != "":
        #     filter_package_data_by_id = TravelPackagesApplication.objects.filter(employee_ref=id, applicants_name=applicants_name, stage=stage)
            filter_package_data = [i for i in filter_package_data_by_id if i.travel_client_ref.client_name == client_name]
        elif applicants_name != "" and client_name != "":
            filter_package_data_by_id = TravelPackagesApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
            filter_package_data = [i for i in filter_package_data_by_id if i.travel_client_ref.client_name == client_name]
        elif applicants_name != "":
            filter_package_data = TravelPackagesApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
        elif created_on != "":
            created_on_List = created_on.split("-")      
            x = datetime.date(int(created_on_List[0]), int(created_on_List[1]), int(created_on_List[2])) 
            filter_package_data_by_id = TravelPackagesApplication.objects.filter(employee_ref=id)
            filter_package_data = [i for i in filter_package_data_by_id if i.created_on.date() == x]
        elif tentative_payment_date != "":
            tentative_payment_date_List = tentative_payment_date.split("-")      
            x = datetime.date(int(tentative_payment_date_List[0]), int(tentative_payment_date_List[1]), int(tentative_payment_date_List[2])) 
            filter_package_data_by_id = TravelPackagesApplication.objects.filter(employee_ref=id)
            filter_package_data = [i for i in filter_package_data_by_id if i.tentative_payment_date.date() == x]
        elif status != "select":
            filter_package_data = TravelPackagesApplication.objects.filter(employee_ref=id, status=status)
        elif stage != "select stage":
            filter_package_data = TravelPackagesApplication.objects.filter(employee_ref=id, stage=stage)
        elif client_name != "":
            filter_package_data_by_id = TravelPackagesApplication.objects.filter(employee_ref=id)
            filter_package_data = [i for i in filter_package_data_by_id if i.travel_client_ref.client_name == client_name]
        else:
            filter_package_data = TravelPackagesApplication.objects.filter(employee_ref=id)
        
        package_data = TravelPackagesApplication.objects.filter(employee_ref=id).order_by("departure_date")
        return render(request, "travel/packages/all_list.html", {"package_data": package_data, "filter_package_data": filter_package_data})


# TICKETS PACKAGE
class TicketsPackages(TemplateView):

    def get(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        filter_ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id)
        ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id).order_by("departure_date")
        return render(request, "travel/tickets/all_list.html", {"ticket_data": ticket_data, "filter_ticket_data": filter_ticket_data})
    
    def post(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        applicants_name = request.POST['applicants_name']
        client_name = request.POST['client_name']
        stage = request.POST['stage']
        status = request.POST['status']
        created_on = request.POST['created_on']
        departure_date = request.POST['departure_date'] 
        
        if applicants_name != "" and client_name != "" and status != "select" and stage != "select stage" and created_on != "" and departure_date != "":
            created_on_List = created_on.split("-")      
            cx = datetime.date(int(created_on_List[0]), int(created_on_List[1]), int(created_on_List[2]))
            departure_date_List = departure_date.split("-")      
            tx = datetime.date(int(departure_date_List[0]), int(departure_date_List[1]), int(departure_date_List[2])) 
            filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(employee_ref=id, applicants_name=applicants_name, stage=stage, status=status)
            filter_ticket_data = [i for i in filter_ticket_data_by_id if i.travel_client_ref.client_name == client_name and i.created_on.date() == cx and i.departure_date.date() == tx]
        elif applicants_name != "" and client_name != "" and status != "select" and stage != "select stage":
            filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(employee_ref=id, applicants_name=applicants_name, stage=stage, status=status)
            filter_ticket_data = [i for i in filter_ticket_data_by_id if i.travel_client_ref.client_name == client_name]
        elif applicants_name != "" and client_name != "":
            filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
            filter_ticket_data = [i for i in filter_ticket_data_by_id if i.travel_client_ref.client_name == client_name]
        # elif applicants_name != "" and client_name != "":
        #     filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
        #     filter_ticket_data = [i for i in filter_ticket_data_by_id if i.travel_client_ref.client_name == client_name]
        elif applicants_name != "":
            filter_ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id, applicants_name=applicants_name)
        elif created_on != "":
            created_on_List = created_on.split("-")      
            x = datetime.date(int(created_on_List[0]), int(created_on_List[1]), int(created_on_List[2])) 
            filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(employee_ref=id)
            filter_ticket_data = [i for i in filter_ticket_data_by_id if i.created_on.date() == x]
        elif departure_date != "":
            tentative_payment_date_List = departure_date.split("-")      
            x = datetime.date(int(tentative_payment_date_List[0]), int(tentative_payment_date_List[1]), int(tentative_payment_date_List[2])) 
            filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(employee_ref=id)
            filter_ticket_data = [i for i in filter_ticket_data_by_id if i.departure_date.date() == x]
        elif status != "select":
            filter_ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id, status=status)
        elif stage != "select stage":
            filter_ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id, stage=stage)
        elif client_name != "":
            filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(employee_ref=id)
            filter_ticket_data = [i for i in filter_ticket_data_by_id if i.travel_client_ref.client_name == client_name]
        else:
            filter_ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id)

        ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id).order_by("departure_date")
        return render(request, "travel/tickets/all_list.html", {"ticket_data": ticket_data, "filter_ticket_data": filter_ticket_data})


    
class TPCustomerDetails(TemplateView):

    template_name = "travel/tickets/customer_details.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)

class TPTransportDetails(TemplateView):

    template_name = "travel/tickets/transport_details.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)
    
class TPPayments(TemplateView):

    template_name = "travel/tickets/payments.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


############################
# ADMIN PAGES
############################


# AGENTS VIEW
class TAdminAgents(TemplateView):

    template_name = "travel/admin/agents.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        updated_context = super().get_context_data(**kwargs)
        updated_context['agents_list'] = VBSEmployeeDetails.objects.all()

        return updated_context  

class TAdminClients(TemplateView):

    template_name = "travel/admin/clients.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        updated_context = super().get_context_data(**kwargs)
        updated_context['clients_list'] = TravelClient.objects.all()

        return updated_context
    
class TAdminPayments(TemplateView):

    template_name = "travel/admin/payments.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


class TAdminFollowups(TemplateView):

    template_name = "travel/admin/followups.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


class TAdminAgentAccounts(TemplateView):

    template_name = "travel/admin/account_mgmt.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        updated_context =  super().get_context_data(**kwargs)
        updated_context['agents_list'] = User.objects.filter(groups__name='travel_agent')

        return updated_context