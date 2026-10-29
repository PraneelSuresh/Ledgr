from django.shortcuts import render, redirect
from django.http import JsonResponse
from finance.models import Transaction, User
from finance.forms import TransactionForm

def about(request):
    return render(request, "finance/about.html")

def ping_json(request):
    return JsonResponse({"status": "ok"})

def transaction_list(request):
    transactions = Transaction.objects.select_related('category', 'account').order_by("-date", "-created_at")
    context = {"transactions" : transactions}
    return render(request, "finance/transactions.html", context)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = User.objects.get(username="demo")
            transaction.save()
            return redirect("finance:transaction_list")
    else:
        form = TransactionForm()
    return render(request, "finance/transaction_form.html", {"form" : form})

