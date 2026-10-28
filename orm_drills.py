import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection, reset_queries
from django.conf import settings
from finance.models import Transaction, Account, Category, User
# Enable query logging
settings.DEBUG = True


reset_queries()
for acct in Account.objects.all():
    for tx in acct.transactions.all():   # ← iterating, not counting
        print(acct.name, tx.description)
print(f"Query count: {len(connection.queries)}")
