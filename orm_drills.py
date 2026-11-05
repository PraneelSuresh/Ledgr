import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection, reset_queries
from django.conf import settings
from finance.models import Transaction, Account, Category, User
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import request
# Enable query logging
settings.DEBUG = True


reset_queries()
bucket_data = Transaction.objects.filter(user__username="demo", date__month=10, kind="expense").values("bucket").annotate(total=Sum("amount"))
