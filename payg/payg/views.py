from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.base import TemplateView

from braces.views import SetHeadlineMixin

class IndexView(SetHeadlineMixin, TemplateView):
    headline = 'Home Page'
    template_name = 'index.html'


def handler404(request):
    response = render_to_response('error/base.html', {'error_code': 404},
        context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('error/base.html', {'error_code': 500},
        context_instance=RequestContext(request))
    response.status_code = 500
    return response