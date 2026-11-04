import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection, reset_queries
from django.conf import settings
from finance.models import Transaction, Account, Category, User
from django.db.models import Q
# Enable query logging
settings.DEBUG = True


reset_queries()
today = datetime.date.today()
this_week = today.isocalendar().week
print(Transaction.objects.filter(Q(date__week=datetime.date.today().isocalendar().week) & Q(date__year=datetime.date.today().isocalendar().year)))
print(datetime.date.today().month)
print(datetime.date.today().year)
