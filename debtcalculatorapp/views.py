from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render as rd

from debtcalculatorapp.forms import *


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


def login_form(request):
    context = {
        'currencies': Currency.objects.all()
    }
    return render(request, "debtcalculatorapp/login.html", context)


@transaction.atomic
def register(request):
    errors = {}
    user_form = UserForm(request.POST)

    if user_form.is_valid():
        user = user_form.save()
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            user.profile = profile
            user.save()
            for member_name in request.POST.getlist('members[]'):
                member_form = MemberForm({
                    'name': member_name,
                    'profile': profile
                })
                if member_form.is_valid():
                    member = member_form.save(commit=False)
                    member.profile = profile
                    member.save()
                else:
                    errors.update(member_form.errors)
                    break

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({}, status=200)
        else:
            errors.update(profile_form.errors)
    else:
        errors.update(user_form.errors)

    return JsonResponse(errors, status=400)
