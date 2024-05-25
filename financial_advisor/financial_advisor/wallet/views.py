from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from financial_advisor.wallet.models import Expense
from financial_advisor.wallet.models import Income


# Create your views here.
@login_required
def index(request):
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    return render(
        request,
        "wallet/index.html",
        {"expenses": expenses, "incomes": incomes},
    )
