from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# from django.db.models.signals import post_save
# from django.dispatch import receiver


class Currency(models.Model):
    full_name = models.CharField(
        max_length=100,
        blank=False
    )

    code = models.CharField(
        max_length=3,
        blank=False,
        unique=True
    )

    def __str__(self):
        return self.code


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

    def __str__(self):
        return f"1 {self.profile.base_currency.code} = {self.rate} {self.secondary_currency.code}"


class Member(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT
    )

    name = models.CharField(
        max_length=30,
        blank=False,
        unique=True
    )

    def __str__(self):
        return self.profile.user.username + ": " + self.name


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

    content = models.TextField(
        max_length=200,
        blank=False
    )

    def __str__(self):
        date = self.date_time.isoformat()[:10]
        return f"[{date}] {self.lender.name}: {self.content[:25]}"
