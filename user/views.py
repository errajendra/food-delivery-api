from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser as User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *
from meal.models import *
from datetime import date
from .forms import ProfileForm


@login_required
def index(request):
    """ Dashbord Page."""
    total_user = CustomUser.objects.filter(is_active=True).count()
    total_meal = MealType.objects.all().count()
    total_plan = Plan.objects.all().count()
    total_plan_purchase = PlanPurchase.objects.filter(
        remaining_meals__gt=0, status=True).count()
    today = date.today()

    # Count the MealRequestDaily objects with the date field matching today's date
    meal_requests = MealRequestDaily.objects.filter(date__date=today).order_by('date')
    today_meal_request_count = meal_requests.count()
    if request.user.is_delivery_person:
        meal_requests_delivery_person = MealRequestDaily.objects.filter(
            date__date=today, delivery_person = request.user).order_by('date')
    else:
        meal_requests_delivery_person = []
    total_meal_request_delivery_person = MealRequestDaily.objects.filter(
        date__date=today, delivery_person = request.user).count()

    context = {
        "total_user":total_user,
        "total_meal":total_meal,
        "total_plan":total_plan,
        "total_plan_purchase":total_plan_purchase,
        "today_meal_request": today_meal_request_count,
        "meal_requests":meal_requests,
        "meal_requests_delivery_person":meal_requests_delivery_person,
        "total_meal_request_delivery_person":total_meal_request_delivery_person
    }
    return render(request, 'user/index.html', context)


def admin_login(request):
    """ Admin Login Method. """
    message = None

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            user = None
        if user and (user.is_staff or user.is_delivery_person or user.is_cook):
            if user.check_password(password):
                login(request, user)
                if user.is_cook:
                    return redirect('daily_meal_request_list')
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('index')

        message = "Invalid Credentials."

    return render(request, 'user/login.html', {'message': message})


@login_required
def user_logout(request):
    """ Logout method for users"""
    logout(request)
    return redirect('login')


@login_required
def user_list(request):
    """ All Customers Listing. """
    context = {
        'title': "Users",
        'users': User.objects.filter(is_staff=False)
    }
    return render(request, 'user/list.html', context)


def user_profile(request):
    if request.method == 'POST' or request.FILES:
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Redirect to the profile page or any other appropriate page after a successful update.
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'user/profile.html', {'form': form})
