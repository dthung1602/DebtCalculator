from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from debtcalculatorapp.models import *


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name']


class ExchangeRateForm(ModelForm):
    class Meta:
        model = ExchangeRate
        fields = ['profile', 'secondary_currency', 'rate']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['base_currency']


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        # https://stackoverflow.com/questions/54013009/django-cant-validate-multi-value-field-sent-by-jquery
        fields = ['date_time', 'content', 'lender', 'total', 'currency', 'exchange_fees']
