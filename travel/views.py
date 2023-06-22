from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from travel.auth.login import OrgAuth
from django.contrib.auth.models import User

# importing models
from .models import (
    TravelClient
)

# Create your views here.


def LoginView(request):
    
    is_validated = None
    role = None

    if request.method == 'POST':

        # getting if user authenticated or not
        org_auth_obj = OrgAuth(request, request.POST.get('email'), request.POST.get('password'))

        # sets the message if user is valid
        is_validated = org_auth_obj.return_if_is_authenticated()

        # returns the admin/employee for travel/recruitment
        role = org_auth_obj.role_redirect()
        
    return render(request, "travel/auth/login.html" if role is None else role, {'auth_validated':is_validated})


# TRAVEL VISA VIEWS
class TravelVISA(TemplateView):

    template_name = 'travel/visa/all_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


class TVDetailProcessing(TemplateView):

    template_name = "travel/visa/detail_processing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)
    

class TVDocumentProcessing(TemplateView):

    template_name = "travel/visa/document_processing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


class TVPaymentProcessing(TemplateView):

    template_name = "travel/visa/payment_processing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


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

    template_name = "travel/packages/all_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


# TICKETS PACKAGE
class TicketsPackages(TemplateView):

    template_name = "travel/tickets/all_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)
    
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
        return super().get_context_data(**kwargs)
    
class TAdminPayments(TemplateView):

    template_name = "travel/admin/payments.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


class TAdminFollowups(TemplateView):

    template_name = "travel/admin/followups.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        
        return super().get_context_data(**kwargs)



class TAdminClients(TemplateView):

    template_name = "travel/admin/clients.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        updated_context = super().get_context_data(**kwargs)
        updated_context['clients_list'] = TravelClient.objects.all()

        return updated_context


class TAdminAgentAccounts(TemplateView):

    template_name = "travel/admin/account_mgmt.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        updated_context = super().get_context_data(**kwargs)
        updated_context['agents_list'] = User.objects.filter(groups__name='travel_agent')

        return updated_context
    
