from django.shortcuts import render
from django.http import JsonResponse
from finance.models import Transaction

def about(request):
    return render(request, "finance/about.html")

def ping_json(request):
    return JsonResponse({"status": "ok"})

def transaction_list(request):
    transactions = Transaction.objects.select_related('category', 'account').order_by("-date", "-created_at")
    context = {"transactions" : transactions}
    return render(request, "finance/transactions.html", context)



