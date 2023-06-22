from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class RCTRCandidate(TemplateView):

    template_name = 'recruitment/recruiter/candidate.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)