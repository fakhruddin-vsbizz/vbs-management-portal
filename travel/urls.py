from . import views
from django.urls import path
from travel.admin.apis.add_new_agent import CreateNewAgentView
from travel.admin.apis.add_new_client import TAdminCreateClient
from travel.admin.apis.edit_agent import TAdminEditAgent
from travel.visa.apis.visa_application__data_entry import TravelApplicationInitiateAPIView
from travel.packages.apis.packages__create import TravelPackagesActionHandlerAPI
from travel.tickets.apis.tickets__crud import TravelTicketsActionHandlerAPI

urlpatterns = [
    path('auth/login', views.LoginView, name='login-view'), # type: ignore
    path('auth/logout', views.logout_view, name='logout-view'),

    # travel visa urls
    path('visa/application', views.TravelVISA.as_view(), name='visa-application'),
    path('visa/application/<str:app_pk>/detail_processing', views.TVDetailProcessing.as_view(), name='visa-detail-processing'),
    path('visa/application/<str:app_pk>/document_processing', views.TVDocumentProcessing.as_view(), name='visa-document-processing'),
    path('visa/application/<str:app_pk>/payment_processing', views.TVPaymentProcessing.as_view(), name='visa-payment-processing'),

    # travel packages urls
    path('packages/application', views.TravelPackages.as_view(), name='package-application'),
    path('packages/application/<str:app_pk>/package_selection', views.TPPackageSelection.as_view(), name='packages-package-selection'),
    path('packages/application/<int:app_pk>/customer_invoicing', views.TPCustomerInvoicing.as_view(), name='packages-customer-invoicing'),
    path('packages/application/<int:app_pk>/vendor_management', views.TPVendorPayments.as_view(), name='packages-vendor-payments'),

    # tickets urls
    path('tickets/application', views.TicketsPackages.as_view(), name='tickets-application'),
    path('tickets/application/<str:app_pk>/customer_details', views.TPCustomerDetails.as_view(), name='tickets-customer-details'),
    path('tickets/application/<int:app_pk>/transport_details', views.TPTransportDetails.as_view(), name='tickets-transport-details'),
    path('tickets/application/<int:app_pk>/payments', views.TPPayments.as_view(), name='tickets-payments'),

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
    path('api/travel_visa_stage_1', TravelApplicationInitiateAPIView.as_view(), name='travel-visa-stage1-api'),
    path('api/client_details/<int:id>', views.ClientDetails.as_view(), name='client_details-api'),
    path('api/agent_details/<int:id>', views.AgentsDetails.as_view(), name='agent_details-api'),
    path('api/travel_packages_crud', TravelPackagesActionHandlerAPI.as_view(), name='travel-packages-crud-api'),
    path('api/travel_tickets_crud', TravelTicketsActionHandlerAPI.as_view(), name='travel-tickets-crud-api'),
    # TravelTicketsActionHandlerAPI
]