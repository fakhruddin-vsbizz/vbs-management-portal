from . import views
from django.urls import path
from travel.admin.apis.add_new_agent import CreateNewAgentView
from travel.admin.apis.add_new_client import TAdminCreateClient
from travel.admin.apis.edit_agent import TAdminEditAgent

urlpatterns = [
    path('auth/login', views.LoginView, name='login-view'),
    path('auth/logout', views.logout_view, name='logout-view'),

    # travel visa urls
    path('visa/application', views.TravelVISA.as_view(), name='visa-application'),
    path('visa/application/new/detail_processing', views.TVDetailProcessing.as_view(), name='visa-detail-processing'),
    path('visa/application/new/document_processing', views.TVDocumentProcessing.as_view(), name='visa-document-processing'),
    path('visa/application/new/payment_processing', views.TVPaymentProcessing.as_view(), name='visa-payment-processing'),

    # travel packages urls
    path('packages/application', views.TravelPackages.as_view(), name='package-application'),
    path('packages/application/new/package_selection', views.TPPackageSelection.as_view(), name='packages-package-selection'),
    path('packages/application/new/customer_invoicing', views.TPCustomerInvoicing.as_view(), name='packages-customer-invoicing'),
    path('packages/application/new/vendor_management', views.TPVendorPayments.as_view(), name='packages-vendor-payments'),

    # tickets urls
    path('tickets/application', views.TicketsPackages.as_view(), name='tickets-application'),
    path('tickets/application/new/customer_details', views.TPCustomerDetails.as_view(), name='tickets-customer-details'),
    path('tickets/application/new/transport_details', views.TPTransportDetails.as_view(), name='tickets-transport-details'),
    path('tickets/application/new/payments', views.TPPayments.as_view(), name='tickets-payments'),

    # admin urls
    # agents
    path('admin/agents', views.TAdminAgents.as_view(), name='admin-agents'),
    path('admin/payments', views.TAdminPayments.as_view(), name='admin-payments'),
    path('admin/followups', views.TAdminFollowups.as_view(), name='admin-followups'),
    path('admin/agentacc', views.TAdminAgentAccounts.as_view(), name='admin-agent-mgmt'),
    path('admin/clients', views.TAdminClients.as_view(), name='admin-clients'),

    # apis path
    path('api/create_new_agent', CreateNewAgentView.as_view(), name='employee-creation-api'),
    path('api/create_new_client', TAdminCreateClient.as_view(), name='client-creation-api'),
    path('api/create_new_client', TAdminCreateClient.as_view(), name='client-creation-api'),
    path('api/edit_travel_agent_details', TAdminEditAgent.as_view(), name='agent-travel-edit-api'),
    # TAdminEditAgent
]