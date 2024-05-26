from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import DecimalField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Financial Advisor.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    country = CharField("Country", blank=True, max_length=255, default="Kazakhstan")

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


    @property
    def cash(self):
        total_income = self.income_set.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = self.expense_set.aggregate(Sum('amount'))['amount__sum'] or 0
        return total_income - total_expense