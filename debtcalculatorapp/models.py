from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class Currency(models.Model):
    full_name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=3,
        unique=True
    )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    end_date = models.DateTimeField(
        null=True
    )

    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    @property
    def has_ended(self):
        return self.end_date is None

    def end_now(self):
        self.end_date = datetime.now()
        self.save()


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class ExchangeRate(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    secondary_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    rate = models.DecimalField(
        max_digits=18,
        decimal_places=6
    )


class Member(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT
    )

    name = models.CharField(
        max_length=30,
        unique=True
    )


class Payment(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    date_time = models.DateTimeField()

    lender = models.ForeignKey(
        Member,
        on_delete=models.PROTECT,
        related_name='lender'
    )

    debtors = models.ManyToManyField(
        Member,
        related_name='debtor'
    )

    total = models.DecimalField(
        max_digits=16,
        decimal_places=2
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    exchange_fees = models.DecimalField(
        max_digits=16,
        decimal_places=2
    )
