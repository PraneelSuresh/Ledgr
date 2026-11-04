from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass


class Account(models.Model):
    class Kind(models.TextChoices):
        BANK = "bank", "Bank"
        CASH = "cash", "Cash"
        CARD = "card", "Card"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
    )
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=10, choices=Kind.choices)
    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_account_name_per_user"
            )
        ]

    def __str__(self):
        return f"{self.get_kind_display()} - {self.name}"


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_category_name_per_user"
            )
        ]

    def __str__(self):
        return self.name


class Transaction(models.Model):

    class Kind(models.TextChoices):
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"

    class Bucket(models.TextChoices):
        NEEDS = "needs", "Needs"
        WANTS = "wants", "Wants"
        SAVINGS = "savings", "Savings"
        INVESTMENT = "investment", "Investment"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    kind = models.CharField(max_length=10, choices=Kind.choices, default="Income")
    bucket = models.CharField(max_length=10, choices=Bucket.choices, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    last_modified = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()
        if self.kind == "expense" and not self.bucket:
            raise ValidationError({"bucket": "Bucket is required for expenses."})
        if self.kind == "income" and self.bucket:
            raise ValidationError({"bucket" : "Bucket must be empty for income"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(kind="income", bucket__isnull=True) |
                    models.Q(kind="expense", bucket__isnull=False)
                ),
                name="bucket_must_match_kind"
            ),
            models.CheckConstraint(
                check=(
                    models.Q(amount__gt=0)
                ),
                name="amount_must_be_positive"
            )
        ]

    def __str__(self):
        return f"{self.date} {self.description[:30]} {self.amount} {self.category}"
