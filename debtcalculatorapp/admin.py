from django.contrib import admin

from .models import *

admin.site.register(Currency)
admin.site.register(Profile)
admin.site.register(ExchangeRate)
admin.site.register(Member)
admin.site.register(Payment)
