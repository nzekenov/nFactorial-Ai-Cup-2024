from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()


class CashTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
