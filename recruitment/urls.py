from . import views
from django.urls import path

urlpatterns = [
    path('candidates/', views.RCTRCandidate.as_view(), name='recruiter-candidates'),
]