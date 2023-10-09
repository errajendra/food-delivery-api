from django.shortcuts import render, redirect


def index(request):
    return render(request, "home/dashboard.html")

def logout(request):
    return redirect("login_user")


def transaction(request):
    return render(request, "home/transactions.html")

def setting(request):
    return render(request, "home/settings.html")

def table(request):
    return render(request, "home/tables-bootstrap-tables.html")

def singIn(request):
    return render(request, "accounts/login.html")

def customerList(request):
    return render(request, "home/customer-list.html")

def menuList(request):
    return render(request, "home/menu-list.html")

def subscriptionList(request):
    return render(request, "home/subscription-list.html")