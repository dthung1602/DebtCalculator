from math import ceil

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http.response import JsonResponse
from django.shortcuts import render as rd

from debtcalculatorapp.forms import *


@login_required
def index(request):
    user = request.user
    payment_pages = group_array(
        Payment.objects.filter(profile=user.profile).order_by('-date_time'),
        settings.PAGE_SIZE
    )
    context = {
        'user': user,
        'currencies': Currency.objects.all(),
        'members': Member.objects.filter(profile=user.profile),
        'payment_pages': payment_pages
    }
    return render(request, "debtcalculatorapp/index.html", context)


@login_required
@transaction.atomic
def add(request):
    payment_form = PaymentForm(request.POST)
    profile = request.user.profile

    if payment_form.is_valid():
        payment = payment_form.save(commit=False)
        debtors = validate_debtors(request)
        if debtors:
            payment.profile = profile
            payment.save()
            payment.debtors.set(debtors)
            exchange_rate = payment.currency.exchangerate_set.filter(profile=profile)
            if len(exchange_rate) == 0 and payment.currency != profile.base_currency:
                exchange_rate = ExchangeRate(
                    profile=profile,
                    secondary_currency=payment.currency,
                    rate=1
                )
                exchange_rate.save()
            return JsonResponse({})
    else:
        return JsonResponse(payment_form.errors, status=400)


@login_required
def summarize(request):
    user = request.user
    exchange_rates = ExchangeRate.objects \
        .filter(profile=user.profile) \
        .prefetch_related('secondary_currency')

    members = user.profile.member_set.all()
    member_payments = []

    for debtor in members:
        for lender in members:
            if debtor.id != lender.id:
                member_payments.append(
                    MemberPayment(debtor, lender, exchange_rates)
                )

    context = {
        'user': user,
        'exchange_rates': exchange_rates,
        'members': members,
        'member_payments': member_payments
    }
    return render(request, "debtcalculatorapp/summarize.html", context)


@login_required
def edit_exchange_rate(request):
    post = request.POST.copy()
    del post['csrfmiddlewaretoken']

    exchange_rates = ExchangeRate.objects.filter(id__in=post.keys())
    for exchange_rate in exchange_rates:
        exchange_rate.rate = post[str(exchange_rate.id)]
        exchange_rate.save()

    return JsonResponse({})


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


def validate_debtors(request):
    debtor_ids = request.POST.getlist('debtors[]')
    debtors = Member.objects.filter(id__in=debtor_ids).prefetch_related('profile')

    if len(debtor_ids) > len(debtors) or len(debtor_ids) == 0:
        return False

    for debtor in debtors:
        if debtor.profile.id != request.user.profile.id:
            return False

    return debtors


def group_array(arr, group_size):
    """Divide arr into groups with size at least group_size"""

    arr = list(arr)
    if group_size > 0:
        return [arr[i * group_size:i * group_size + group_size] for i in range(ceil(len(arr) / group_size))]
    return [arr]


class MemberPayment:
    def __init__(self, debtor: Member, lender: Member, all_exchange_rates):
        self.debtor = debtor
        self.lender = lender
        self.total = 0
        self.reasons = []

        payments = Payment.objects \
            .annotate(num_debtors=Count('debtors')) \
            .filter(lender=lender, debtors=debtor)

        exchange_rates = []
        for payment in payments:
            for er in all_exchange_rates:
                if er.id == payment.currency_id:
                    exchange_rates.append(er)
                    break

        for payment, exchange_rate in zip(payments, exchange_rates):
            t = payment.total * exchange_rate.rate + payment.exchange_fees
            self.total += t / payment.num_debtors
            date = payment.date_time.strftime('%m/%d ')
            self.reasons.append(date + payment.content)
