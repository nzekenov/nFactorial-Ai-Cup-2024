from django.conf import settings
from django.db import models
from django.db.models import Sum

from financial_advisor.users.models import User


def get_default_user():
    return User.objects.get(username="nzekenov")

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        default=get_default_user
    )

    def __str__(self) -> str:
        return self.name


class CashTransaction(models.Model):
    user = user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        default=get_default_user
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField()

    class Meta:
        abstract = True


class Expense(CashTransaction):
    def __str__(self) -> str:
        return super().__str__()


class Income(CashTransaction):
    def __str__(self) -> str:
        return super().__str__()
