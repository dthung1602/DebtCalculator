from django.contrib.auth.models import User
from django.db import models


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

    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT
    )

    note = models.TextField(
        null=True,
    )

    def __str__(self):
        return self.user.username


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
        return f"{self.profile.base_currency.code} = {self.rate} {self.secondary_currency.code}"


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
        decimal_places=2,
        null=True
    )

    content = models.TextField(
        max_length=200,
        blank=False
    )

    def __str__(self):
        date = self.date_time.isoformat()[:10]
        return f"[{date}] {self.lender.name}: {self.content}"

    @property
    def formatted_date(self):
        return self.date_time.strftime("%a, %b %d %H%p")

    @property
    def debtors_names(self):
        return [debtor.name for debtor in self.debtors.all().order_by('name')]
