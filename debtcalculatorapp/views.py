from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render as rd

from debtcalculatorapp.models import *


def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """Override render function to add information to context for base.html"""

    if context is None:
        context = {}
    context['now'] = datetime.now()
    context['app_version'] = settings.APP_VERSION
    context['contact_email'] = settings.CONTACT_EMAIL
    context['contact_github'] = settings.CONTACT_GITHUB
    context['contact_facebook'] = settings.CONTACT_FACEBOOK

    return rd(request, template_name, context, content_type, status, using)


@login_required
def index(request):
    return HttpResponse("index")


@login_required
def summarize(request):
    return HttpResponse("Summarize")


def login(request):
    context = {
        'currencies': Currency.objects.all()
    }
    return render(request, "debtcalculatorapp/login.html", context)


def register(request):
    context = {
        'currencies': Currency.objects.all()
    }
    return render(request, "debtcalculatorapp/login.html", context)
