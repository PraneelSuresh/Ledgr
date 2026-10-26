from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def ping(request):
    return HttpResponse("pong")

def echo(request, name):
    return HttpResponse(f"Hello {name}!")

def landing(request):
    context = {
        "title": "Ledgr",
        "transactions": [
            {"date": "2026-10-01", "description": "Coffee", "amount": 4.50},
            {"date": "2026-10-02", "description": "Groceries", "amount": 62.30},
            {"date": "2026-10-03", "description": "Salary", "amount": 3500.00},
        ]
    }
    return render(request, "finance/landing.html", context)

def about(request):
    return render(request, "finance/about.html")

def ping_json(request):
    response = {"status" : "ok"}
    return JsonResponse(response)

def view_transactions(request):
    context = {
        "transactions": [
            {"date": "2026-10-01", "description": "Coffee", "amount": 4.50},
            {"date": "2026-10-02", "description": "Groceries", "amount": 62.30},
            {"date": "2026-10-03", "description": "Salary", "amount": 3500.00},
        ]
    }
    return render(request, "finance/transactions.html", context)

def another_echo(request, name, age):
    return HttpResponse(f"Hello, {name}! You are {age} years old.")

