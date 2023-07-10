from typing import Any, Dict
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from travel.auth.login import OrgAuth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .serializers import TravelTicketsApplicationSerializer, TravelPackagesApplicationSerializer, TravelVisaApplicationSerializer, TravelClientSerializer, VBSEmployeeDetailsSerializer
from .variables import COUNTRIES
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from .variables import COUNTRIES, PACKAGE_TYPE, MAJOR_CITIES, TICKETS_TYPE
import datetime
from rest_framework.response import Response
from .models import TravelClient, VBSEmployeeDetails, TravelVisaApplication, TravelPackagesApplication, TravelTicketsApplication

from django import template


# Create your views here.

def LoginView(request):
    
    is_validated = None
    role = None

    if request.method == 'POST':

        # getting if user authenticated or not
        org_auth_obj = OrgAuth(request, request.POST.get('email'), request.POST.get('password'))

        # sets the message if user is valid
        is_validated = org_auth_obj.return_if_is_authenticated()
        print(is_validated)
        
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

class ClientDetails(APIView):
    
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        client_details_data = TravelClient.objects.filter(id=client_id)
        client_visa_data = TravelVisaApplication.objects.filter(travel_client_ref=client_id)
        client_packages_data = TravelPackagesApplication.objects.filter(travel_client_ref=client_id)
        client_ticket_data = TravelTicketsApplication.objects.filter(travel_client_ref=client_id)
        serialize = TravelClientSerializer(client_details_data, many=True)
        serialize1 = TravelVisaApplicationSerializer(client_visa_data, many=True)
        serialize2 = TravelPackagesApplicationSerializer(client_packages_data, many=True)
        serialize3 = TravelTicketsApplicationSerializer(client_ticket_data, many=True)
        
        print(serialize1.data, serialize2.data, serialize3.data)
        Serializer_list = [serialize.data, serialize1.data, serialize2.data, serialize3.data]
        
        content = {
        'status': 1, 
        'responseCode' : status.HTTP_200_OK, 
        'data': Serializer_list,
        }
        
        return JsonResponse(content)

class AgentsDetails(APIView):
    
    def get(self, request, *args, **kwargs):
        emp_id = kwargs.get('id')
        emp_details_data = VBSEmployeeDetails.objects.filter(id=emp_id)
        emp_visa_data = TravelVisaApplication.objects.filter(employee_ref=emp_id)
        emp_packages_data = TravelPackagesApplication.objects.filter(employee_ref=emp_id)
        emp_ticket_data = TravelTicketsApplication.objects.filter(employee_ref=emp_id)
        serialize = VBSEmployeeDetailsSerializer(emp_details_data, many=True)
        serialize1 = TravelVisaApplicationSerializer(emp_visa_data, many=True)
        serialize2 = TravelPackagesApplicationSerializer(emp_packages_data, many=True)
        serialize3 = TravelTicketsApplicationSerializer(emp_ticket_data, many=True)
        
        print(serialize1.data, serialize2.data, serialize3.data)
        Serializer_list = [serialize.data, serialize1.data, serialize2.data, serialize3.data]
        
        content = {
        'status': 1, 
        'responseCode' : status.HTTP_200_OK, 
        'data': Serializer_list,
        }
        
        return JsonResponse(content)

# TRAVEL VISA VIEWS
class TravelVISA(TemplateView):
    
    def get(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        filter_visa_data = TravelVisaApplication.objects.filter(employee_ref=id)
        visa_data = TravelVisaApplication.objects.filter(employee_ref=id).order_by("handover_date")

        return render(request, 'travel/visa/all_list.html', {"visa_data": visa_data, "filter_visa_data": filter_visa_data})
    
    def post(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        
        data = {}
        
        data["employee_ref"] = id.id # type: ignore
        
        for i in request.POST:
            if i == "csrfmiddlewaretoken" or i == "client_name":
                continue
            elif request.POST[i] not in ["", " ", "select stage", "select"]:
                if i not in ["created_on","handover_date"]:
                    data[i] = request.POST[i]
                else:
                    date_List = request.POST[i].split("-")      
                    formatted_date = datetime.date(int(date_List[0]), int(date_List[1]), int(date_List[2]))
                    print(formatted_date, datetime.date(int(date_List[0]), int(date_List[1]), int(date_List[2])))
                    data[i+"__date"] = formatted_date
                
        if request.POST["client_name"] not in ["", " "]:
            filter_visa_data_by_id = TravelVisaApplication.objects.filter(**data)
            filter_visa_data = [i for i in filter_visa_data_by_id if i.travel_client_ref.client_name == request.POST["client_name"]]
        else:
            filter_visa_data = TravelVisaApplication.objects.filter(**data)
        
        visa_data = TravelVisaApplication.objects.filter(employee_ref=id).order_by("handover_date")
        return render(request, 'travel/visa/all_list.html', {"visa_data": visa_data, "filter_visa_data": filter_visa_data})
    



class TVDetailProcessing(View):
    def get(self, request, *args, **kwargs):

        travel_visa_obj = None

        if kwargs['app_pk'] == "new":
            pass
        else:
            app_id = int(kwargs['app_pk'])
            travel_visa_obj = TravelVisaApplication.objects.get(id=app_id)

        context = {}
        context['app_id'] = kwargs['app_pk']
        context['all_travel_clients'] = TravelClient.objects.all()
        context['countries'] = COUNTRIES
        context['travel_visa_obj'] = travel_visa_obj

        return render(request, 'travel/visa/detail_processing.html', context)
    

class TVDocumentProcessing(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['app_id'] = kwargs['app_pk']

        travel_visa_obj = TravelVisaApplication.objects.get(id=kwargs['app_pk'])
        context['travel_visa_obj'] = travel_visa_obj
        return render(request, 'travel/visa/document_processing.html', context)


class TVPaymentProcessing(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context['app_id'] = kwargs['app_pk']

        travel_visa_obj = TravelVisaApplication.objects.get(id=kwargs['app_pk'])
        context['travel_visa_obj'] = travel_visa_obj
        print()

        return render(request, 'travel/visa/payment_processing.html', context)


# TRAVEL PACKAGE
class TPPackageSelection(View):

    def get(self, request, *args, **kwargs):

        travel_packages_obj = None

        if kwargs['app_pk'] == "new":
            pass
        else:
            app_id = int(kwargs['app_pk'])
            travel_packages_obj = TravelPackagesApplication.objects.get(id=app_id)

        context = {}

        context['app_id'] = kwargs['app_pk']
        context['packages_type'] = PACKAGE_TYPE
        context['all_cities'] = MAJOR_CITIES
        context['all_travel_clients'] = TravelClient.objects.all()
        context['travel_packages_obj'] = travel_packages_obj

        print(context['all_travel_clients'])
        

        return render(request, 'travel/packages/package_selection.html', context)
    

class TPCustomerInvoicing(View):

    def get(self, request, *args, **kwargs):
        context = {}

        context['app_id'] = kwargs['app_pk']
        context['travel_packages_obj'] = TravelPackagesApplication.objects.get(id=kwargs['app_pk'])

        return render(request, 'travel/packages/customer_invoicing.html', context)

    
    
class TPVendorPayments(View):

    def get(self, request, *args, **kwargs):
        context = {}

        context['app_id'] = kwargs['app_pk']
        context['travel_packages_obj'] = TravelPackagesApplication.objects.get(id=kwargs['app_pk'])

        return render(request, 'travel/packages/vendor_management.html', context)


class TravelPackages(TemplateView):

    def get(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        filter_package_data = TravelPackagesApplication.objects.filter(employee_ref=id)
        package_data = TravelPackagesApplication.objects.filter(employee_ref=id).order_by("departure_date")
        return render(request, "travel/packages/all_list.html", {"package_data": package_data, "filter_package_data": filter_package_data})
    
    def post(self, request):
        id = VBSEmployeeDetails.objects.get(employee_auth_user_ref_id=request.user.id)
        
        data = {}
        
        data["employee_ref"] = id.id # type: ignore
        
        for i in request.POST:
            if i == "csrfmiddlewaretoken" or i == "client_name":
                continue
            elif request.POST[i] not in ["", " ", "select stage", "select"]:
                if i not in ["created_on","tentative_payment_date"]:
                    data[i] = request.POST[i]
                else:
                    date_List = request.POST[i].split("-")      
                    formatted_date = datetime.date(int(date_List[0]), int(date_List[1]), int(date_List[2]))
                    print(formatted_date, datetime.date(int(date_List[0]), int(date_List[1]), int(date_List[2])))
                    data[i+"__date"] = formatted_date
                
        if request.POST["client_name"] not in ["", " "]:
            filter_package_data_by_id = TravelPackagesApplication.objects.filter(**data)
            filter_package_data = [i for i in filter_package_data_by_id if i.travel_client_ref.client_name == request.POST["client_name"]]
        else:
            filter_package_data = TravelPackagesApplication.objects.filter(**data)
              
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
                
        data = {}
        
        data["employee_ref"] = id.id # type: ignore
        
        for i in request.POST:
            if i == "csrfmiddlewaretoken" or i == "client_name":
                continue
            elif request.POST[i] not in ["", " ", "select stage", "select"]:
                if i not in ["created_on","departure_date"]:
                    data[i] = request.POST[i]
                else:
                    date_List = request.POST[i].split("-")      
                    formatted_date = datetime.date(int(date_List[0]), int(date_List[1]), int(date_List[2]))
                    print(formatted_date, datetime.date(int(date_List[0]), int(date_List[1]), int(date_List[2])))
                    data[i+"__date"] = formatted_date
                
        if request.POST["client_name"] not in ["", " "]:
            filter_ticket_data_by_id = TravelTicketsApplication.objects.filter(**data)
            filter_ticket_data = [i for i in filter_ticket_data_by_id if i.travel_client_ref.client_name == request.POST["client_name"]]
        else:
            filter_ticket_data = TravelTicketsApplication.objects.filter(**data)
            
        ticket_data = TravelTicketsApplication.objects.filter(employee_ref=id).order_by("departure_date")
        return render(request, "travel/tickets/all_list.html", {"ticket_data": ticket_data, "filter_ticket_data": filter_ticket_data})


    
class TPCustomerDetails(View):

    def get(self, request, *args, **kwargs):

        travel_packages_obj = None

        if kwargs['app_pk'] == "new":
            pass
        else:
            app_id = int(kwargs['app_pk'])
            travel_packages_obj = TravelTicketsApplication.objects.get(id=app_id)

        context = {}

        context['app_id'] = kwargs['app_pk']
        context['tickets_type'] = TICKETS_TYPE
        context['all_cities'] = MAJOR_CITIES
        context['all_travel_clients'] = TravelClient.objects.all()
        context['travel_tickets_obj'] = travel_packages_obj

        return render(request, "travel/tickets/customer_details.html", context)


class TPTransportDetails(View):

    def get(self, request, *args, **kwargs):

        context = {}
        

        context['app_id'] = kwargs['app_pk']
        context['travel_tickets_obj'] = TravelTicketsApplication.objects.get(id=kwargs['app_pk'])

        return render(request, 'travel/tickets/transport_details.html', context)

    
class TPPayments(View):

    def get(self, request, *args, **kwargs):

        context = {}
    
        context['app_id'] = kwargs['app_pk']
        context['travel_tickets_obj'] = TravelTicketsApplication.objects.get(id=kwargs['app_pk'])

        return render(request, 'travel/tickets/payments.html', context)


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



