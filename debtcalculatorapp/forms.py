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
        fields = ['profile', 'date_time', 'lender', 'debtors', 'total', 'currency']
