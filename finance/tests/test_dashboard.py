import pytest
import datetime
from django.urls import reverse
from finance.models import Transaction, User, Account, Category


@pytest.mark.django_db
def test_dashboard_totals(client):
    user = User.objects.create_user(username="test_dash", password="pass")
    account = Account.objects.create(user=user, name="Bank", kind="bank")
    category = Category.objects.create(user=user, name="Food")

    today = datetime.date.today()

    # This month's data
    Transaction.objects.create(user=user, account=account, category=category, kind="income", amount=1000, date=today)
    Transaction.objects.create(user=user, account=account, category=category, kind="income", amount=500, date=today)
    Transaction.objects.create(user=user, account=account, category=category, kind="expense", bucket="needs", amount=200, date=today)

    # Last month's data (should be ignored by the dashboard)
    last_month = today - datetime.timedelta(days=32)
    Transaction.objects.create(user=user, account=account, category=category, kind="income", amount=9999, date=last_month)

    client.force_login(user)
    response = client.get(reverse("finance:view_dashboard"))

    assert response.status_code == 200

    # Check that the context passed to the template has the right math
    assert response.context["income"] == 1500  # (1000 + 500)
    assert response.context["expense"] == 200
    assert response.context["net"] == 1300     # (1500 - 200)
