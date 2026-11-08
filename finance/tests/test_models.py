from django.core.exceptions import ValidationError
import datetime
from finance.models import Account, User, Category, Transaction
import pytest

@pytest.mark.django_db
def test_expense_requires_bucket():
    user = User.objects.create_user(username="test_model", password="pass")
    account = Account.objects.create(user=user, name="Bank", kind="bank")
    category = Category.objects.create(user=user, name="Food")

    tx = Transaction(
        user=user, account=account, category=category,
        kind="expense", bucket=None, amount=100, date=datetime.date.today()
    )

    # We expect a ValidationError when we call full_clean()
    with pytest.raises(ValidationError) as exc_info:
        tx.full_clean()

    # Verify the error is specifically about the bucket
    assert "bucket" in exc_info.value.message_dict

@pytest.mark.django_db
def test_income_must_not_have_bucket():
    user = User.objects.create_user(username="test_model2", password="pass")
    account = Account.objects.create(user=user, name="Bank", kind="bank")
    category = Category.objects.create(user=user, name="Salary")

    tx = Transaction(
        user=user, account=account, category=category,
        kind="income", bucket="needs", amount=100, date=datetime.date.today()
    )

    with pytest.raises(ValidationError) as exc_info:
        tx.full_clean()

    assert "bucket" in exc_info.value.message_dict
