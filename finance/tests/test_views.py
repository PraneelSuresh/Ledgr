import pytest
from django.urls import reverse
from finance.models import Account, User, Transaction, Category


@pytest.mark.django_db
def test_user_cannot_edit_other_users_transaction(client):
    user_a = User.objects.create(username="alice", email="alice@borderland.com", password="pass")
    user_b = User.objects.create(username="bob", email="bob@saulgoodman.com", password="youhaverights")

    account_a = Account.objects.create(user=user_a, name="A Bank", kind="bank")
    category_a = Category.objects.create(user=user_a, name="A Food")
    transaction_a = Transaction.objects.create(user=user_a, account=account_a, category=category_a, kind="income", amount=20, date="2026-11-05", description="test transaction")

    client.force_login(user_b)

    url = reverse("finance:edit_transaction", args=[transaction_a.pk])

    response = client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_user_cannot_delete_other_users_transaction(client):
    user_a = User.objects.create(username="alice", email="alice@borderland.com", password="pass")
    user_b = User.objects.create(username="bob", email="bob@saulgoodman.com", password="youhaverights")

    account_a = Account.objects.create(user=user_a, name="A Bank", kind="bank")
    category_a = Category.objects.create(user=user_a, name="A Food")
    transaction_a = Transaction.objects.create(user=user_a, account=account_a, category=category_a, kind="income", amount=20, date="2026-11-05", description="test transaction")

    client.force_login(user_b)

    url = reverse("finance:delete_transaction", args=[transaction_a.pk])

    response = client.get(url)

    assert response.status_code == 404

