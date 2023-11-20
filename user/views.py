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
    total_meal = Meal.objects.all().count()
    total_plan = Plan.objects.all().count()
    total_plan_purchase = PlanPurchase.objects.all().count()
    today = date.today()

    # Count the MealRequestDaily objects with the date field matching today's date
    today_meal_request = MealRequestDaily.objects.filter(date__date=today).count()
    meal_requests = MealRequestDaily.objects.filter(date__date=today).order_by('date')
    meal_requests_delivery_person = MealRequestDaily.objects.filter(date__date=today, delivery_person = request.user).order_by('date')
    
    total_meal_request_delivery_person = MealRequestDaily.objects.filter(date__date=today, delivery_person = request.user).count()

    context = {
        "total_user":total_user,
        "total_meal":total_meal,
        "total_plan":total_plan,
        "total_plan_purchase":total_plan_purchase,
        "today_meal_request":today_meal_request,
        "meal_requests":meal_requests,
        "meal_requests_delivery_person":meal_requests_delivery_person,
        "total_meal_request_delivery_person":total_meal_request_delivery_person
    }
    return render(request, 'user/index.html', context)

def admin_login(request):
    """ Admin Login Method. """
    message = None

    if request.method == "POST":
        mobile_number = request.POST['mobile_number']
        print(mobile_number)
        password = request.POST['password']

        try:
            user = User.objects.get(mobile_number=mobile_number, is_staff=True)
        except User.DoesNotExist:
            user = None

        if user:
            if user.check_password(password):
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('index')
        else:
            # User is not an admin, check if they are a delivery person
            try:
                user1 = CustomUser.objects.get(mobile_number=mobile_number, is_delivery_person=True, is_active=True)
            except CustomUser.DoesNotExist:
                user1 = None

            if user1 and user1.check_password(password):
                login(request, user1)
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