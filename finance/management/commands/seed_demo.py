from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from decimal import Decimal
from finance.models import Transaction, Account, Category, User
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Seed the database with demo data for Ledgr."

    def handle(self, *args, **options):
        random.seed(42)
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@ledgr.local', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password("demo")
            user.save()
            self.stdout.write(self.style.SUCCESS("Created user 'demo' (password : 'demo')"))
        else:
            self.stdout.write(self.style.NOTICE("User 'demo' already exists. Use username: 'demo', password: 'demo' to log in"))

        accounts_data = [
            {"name": "HDFC Savings", "kind": "bank", "opening_balance": Decimal("50000")},
            {"name": "Wallet", "kind": "cash", "opening_balance": Decimal("2000")},
        ]

        accounts = []
        for data in accounts_data:
            account, _ = Account.objects.get_or_create(
                user=user,
                name=data["name"],
                defaults={
                    "kind": data["kind"],
                    "opening_balance": data["opening_balance"],
                },
            )
            accounts.append(account)
            self.stdout.write(f"Account: {account.name}")

        category_names = ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Salary"]

        categories = {}
        for name in category_names:
            category, _ = Category.objects.get_or_create(user=user, name=name)
            categories[name] = category
            self.stdout.write(f"Category: {category.name}")
        self.stdout.write(self.style.SUCCESS("Created demo categories"))

        EXPENSE_TEMPLATES = [
            ("Groceries", "Food", "needs", Decimal("450")),
            ("Dinner out", "Food", "wants", Decimal("1200")),
            ("Coffee", "Food", "wants", Decimal("300")),
            ("Uber ride", "Transport", "needs", Decimal("800")),
            ("Train pass", "Transport", "needs", Decimal("2200")),
            ("Electricity bill", "Utilities", "needs", Decimal("1800")),
            ("Internet", "Utilities", "needs", Decimal("999")),
            ("Movie tickets", "Entertainment", "wants", Decimal("600")),
            ("Book", "Entertainment", "wants", Decimal("450")),
        ]

        today = date.today()
        transactions_created = 0
        Transaction.objects.filter(user=user).delete()
        for months_ago in range(6):
            month_start = (today.replace(day=1) - timedelta(days=1))
            for _ in range(months_ago):
                month_start = month_start.replace(day=1) - timedelta(days=1)
            month_start = month_start.replace(day=1)

            Transaction.objects.create(
                user=user,
                account=accounts[0],
                category=categories["Salary"],
                kind="income",
                bucket=None,
                amount=Decimal("80000"),
                date=month_start,
                description="Monthly salary",
            )
            transactions_created += 1

            Transaction.objects.create(
                user=user,
                account=accounts[0],
                category=categories["Rent"],
                kind="expense",
                bucket="needs",
                amount=Decimal("25000"),
                date=month_start + timedelta(days=1),
                description="Monthly rent",
            )
            transactions_created += 1

            for _ in range(random.randint(8, 12)):
                desc, cat_name, bucket, base_amount = random.choice(EXPENSE_TEMPLATES)
                jitter = Decimal(str(random.uniform(0.7, 1.3)))
                amount = (base_amount * jitter).quantize(Decimal("0.01"))
                day_offset = random.randint(2, 27)

                Transaction.objects.create(
                    user=user,
                    account=random.choice(accounts),
                    category=categories[cat_name],
                    kind="expense",
                    bucket=bucket,
                    amount=amount,
                    date=month_start + timedelta(days=day_offset),
                    description=desc,
                )
                transactions_created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {transactions_created} transactions"))

        self.stdout.write(self.style.SUCCESS("Seeding demo data complete..."))
