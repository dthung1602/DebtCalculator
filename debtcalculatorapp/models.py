from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    full_name = models.CharField(
        max_length=50
    )

    code = models.CharField(
        max_length=3,
        unique=True
    )


class Entry(models.Model):
    group = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    name = models.CharField(
        max_length=30,
        unique=True
    )

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    end_date = models.DateTimeField(
        null=True
    )

    @property
    def has_ended(self):
        return self.end_date is None

    def end_now(self):
        self.end_date = datetime.now()
        self.save()


class Person(models.Model):
    group = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    name = models.CharField(
        max_length=30,
        unique=True
    )


class Payment(models.Model):
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE
    )

    date_time = models.DateTimeField()

    lender = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='lender'
    )

    debtors = models.ManyToManyField(
        Person,
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
