from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from finance.models import Transaction, Category, Account
from finance.forms import TransactionForm, CategoryForm, CustomUserCreationForm, AuthenticationForm, AccountForm
from django.contrib import messages
from django.contrib.auth import login, logout as django_logout
from django.contrib.auth.decorators import login_required
from finance.filters import KindFilter, TimeFilter
import datetime
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator

def homepage(request):
    if request.user.is_authenticated:
        return redirect("finance:transaction_list")
    return render(request, "finance/homepage.html")

def ping_json(request):
    return JsonResponse({"status": "ok"})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).select_related('category', 'account').order_by("-date", "-created_at")
    kind_filter = KindFilter(request.GET, queryset=transactions)
    transactions = kind_filter.qs
    time_filter = TimeFilter(request.GET, queryset=transactions)
    transactions = time_filter.qs
    paginator = Paginator(transactions, 7)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
    context = {"transactions" : transactions, "time_filter" : time_filter, "kind_filter": kind_filter}
    return render(request, "finance/transactions.html", context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction saved.")
            return redirect("finance:transaction_list")
    else:
        form = TransactionForm(user=request.user)
    return render(request, "finance/transaction_form.html", {"form": form})

@login_required
def view_categories(request):
    form = CategoryForm()
    categories = Category.objects.filter(user=request.user)
    return render(request, "finance/category_form.html", {"form": form,"categories" : categories})

@login_required
def add_category(request):
    form = CategoryForm(request.POST, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("finance:category_list")
        categories = Category.objects.filter(user=request.user)
        return render(request, "finance/category_form.html", {
            "form": form,
            "categories": categories,
            "open_modal": True
        })
    return redirect("finance:category_list")

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    category.delete()
    return redirect("finance:category_list")

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("finance:category_list")
        categories = Category.objects.filter(user=request.user)
        return render(request, "finance/category_form.html", {
            "form": form,
            "categories": categories,
            "open_modal": True
        })
    return redirect("finance:category_list")

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated.")
            return redirect("finance:transaction_list")
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, "finance/transaction_form.html", {"form": form, "is_edit": True})
@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Transaction deleted.")
        return redirect("finance:transaction_list")
    return render(request, "finance/transaction_confirm_delete.html", {"transaction": transaction})

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("finance:transaction_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "finance/register.html", {"form" : form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("finance:transaction_list")


    else:
        form = AuthenticationForm()
    return render(request, "finance/login.html", {"form": form})
@login_required
def logout_user(request):
    django_logout(request)
    request.session.flush()
    return redirect("finance:login_user")
@login_required
def accounts_list(request):
    form = AccountForm(user=request.user)
    accounts = Account.objects.filter(user=request.user)
    return render(request, "finance/accounts.html", {"form": form, "accounts": accounts})

@login_required
def add_account(request):
    form = AccountForm(request.POST, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("finance:accounts_list")
        accounts = Account.objects.filter(user=request.user)
        return render(request, "finance/accounts.html", {"form": form, "accounts": accounts, "open_modal" : True})
    return redirect("finance:accounts_list")

@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == "POST":
        account.delete()
        return redirect("finance:accounts_list")

@login_required
def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("finance:accounts_list")
        accounts = Account.objects.filter(user=request.user)
        return render(request, "finance/accounts.html", {"form": form, "accounts": accounts, "is_edit": True, "open_modal" : True})
    return redirect("finance:accounts_list")
@login_required
def view_dashboard(request):
    this_month = datetime.date.today().month
    this_year = datetime.date.today().year

    income = Transaction.objects.filter(user=request.user, kind="income", date__month=this_month, date__year=this_year).aggregate(total=Sum("amount"))
    total_expense = Transaction.objects.filter(user=request.user, kind="expense", date__month=this_month, date__year=this_year).aggregate(total=Sum("amount"))
    expenses_grouped_by_bucket = list(Transaction.objects.filter(user=request.user, kind="expense", date__month=this_month, date__year=this_year).values("bucket").annotate(total=Sum("amount")))
    expenses_grouped_by_category = list(Transaction.objects.filter(user=request.user, kind="expense", date__month=this_month, date__year=this_year).values("category__name").annotate(total=Sum("amount")))
    six_month_summary = list(Transaction.objects.filter(user=request.user).annotate(month=TruncMonth("date")).values("month", "kind").annotate(total=Sum("amount")).order_by("-month")[:12])
    for item in six_month_summary:
        item["month"] = item["month"].strftime("%b %Y")

    if total_expense["total"] == None:
        total_expense["total"] = 0
    if income["total"] == None:
        income["total"] = 0

    net = income["total"] - total_expense["total"]

    return render(request, 'finance/dashboard.html' ,{"income": income["total"], "expense": total_expense["total"], "net": net, "expenses_grouped_by_bucket": expenses_grouped_by_bucket, "expenses_grouped_by_category": expenses_grouped_by_category, "six_month_summary": six_month_summary})
