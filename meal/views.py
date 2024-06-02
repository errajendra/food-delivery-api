from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.db.models import Sum
from .forms import (
    Meal, MealForm, MealTypeForm,
    Plan, PlanForm, MealRequestForm, MealRequestUpdateForm,
    DailyMealMenuForm, PlanPurchaseForm,
    SalesConnectForm, CouponForm, KitchenOffForm,
)
from .models import *
from user.models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import BannerForm


"""
    Meal Type View Functions
"""
def meal_type_add(request):
    form = MealTypeForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('meal_type_list')
    context = {
        "form": form,
        "title": "Add Meal Type Form",
    }
    return render(request, 'meal/form.html', context)


def meal_type_list(request):
    meals = MealType.objects.select_related().all()
    context = {"data": meals, 'title': "Meal Types"}
    return render(request, 'meal/meal-type-list.html', context)


def meal_type_edit(request, id):
    # Edit Category Method
    instance = get_object_or_404(MealType, id=id)
    form = MealTypeForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('meal_type_list')
    context = {
        "title": "Update Meal Type",
        "form": form,
    }
    return render(request, 'meal/form.html', context)


def meal_type_delete(request, id):
    instance = get_object_or_404(MealType, id=id)
    instance.delete()
    return redirect('meal_type_list')



"""
    Meal or Food View Functions
"""
def meal_add(request):
    # Add Category Method
    form = MealForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('meal_list')
    context = {
        "form": form,
        "title": "Add Meal Form",
    }
    return render(request, 'meal/form.html', context)


def meal_list(request):
    # List Categories Method
    meals = Meal.objects.select_related().all()
    context = {"meals": meals, 'title': "Meals"}
    return render(request, 'meal/meal-list.html', context)


def meal_edit(request, id):
    # Edit Category Method
    instance = get_object_or_404(Meal, id=id)
    form = MealForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('meal_list')
    context = {
        "title": "Update Meal",
        "form": form,
    }
    return render(request, 'meal/form.html', context)

def meal_delete(request, id):
    instance = get_object_or_404(Meal, id=id)
    instance.delete()
    return redirect('meal_list')



"""
    Plan View Functions
"""
def plan_add(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            eating_type = ', '.join(request.POST.getlist('eating_type'))
            form.instance.eating_type = eating_type
            # Convert the eating_type field to a list
           
            form.save()
            return redirect('plan_list')
    else:
        form = PlanForm()

    context = {
        "form": form,
        "title": "Add Plan Form",
    }
    return render(request, 'meal/form.html', context)

def plan_list(request):
    plans = Plan.objects.select_related().all()
    context = {"plans": plans, 'title': "Plans"}
    return render(request, 'meal/plan-list.html', context)


def plan_delete(request, id):
    instance = get_object_or_404(Plan, id=id)
    instance.delete()
    return redirect('plan_list')


def plan_edit(request, id):
    instance = get_object_or_404(Plan, id=id)
    form = PlanForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            eating_type = ', '.join(request.POST.getlist('eating_type'))
            form.instance.eating_type = eating_type
            form.save()
            return redirect('plan_list')
    context = {
        "title": "Update Plan",
        "form": form,
    }
    return render(request, 'meal/form.html', context)



"""
Plan Purchese
"""

def plan_purchase_list(request):
    plan_purchase = PlanPurchase.objects.select_related().filter(status=True)
    context = {"plan_purchase": plan_purchase, 'title': "Plan Purchase List"}
    return render(request, 'meal/plan-purchase-list.html', context)


def plan_purchese_add(request):
    if request.method == 'POST':
        form = PlanPurchaseForm(request.POST)
        if form.is_valid():
            plan = get_object_or_404(Plan, id=request.POST.get('plan'))
            user = get_object_or_404(CustomUser, id=request.POST.get('user'))
            transaction = Transaction.objects.create(
                user = user,
                amount = plan.price,
                status = "Success"
            )
            plan_purchese = PlanPurchase.objects.create(
                user = user,
                plan = plan,
                transaction = transaction,
                total_meals = plan.number_of_meals,
                remaining_meals = plan.number_of_meals,
                status = True
            )
            return redirect('plan_purchase_list')
    else:
        form = PlanPurchaseForm()

    context = {
        "form": form,
        "title": "New Plan Purchese Form",
    }
    return render(request, 'meal/form.html', context)


def daily_meal_request_list(request):
    user = request.user
    
    daily_meal_request = MealRequestDaily.objects.select_related().all()
    
    date_filters = ["ALL", "TODAY", "WEEK", "MONTH", "THIS-YEAR"]
    
    date_filter = request.GET.get('date', 'ALL')
    
    date = timezone.datetime.now().date()
    
    if date_filter != 'ALL':
        if date_filter == 'TODAY':
            daily_meal_request = daily_meal_request.filter(date__date=date.today())
        elif date_filter == 'WEEK':
            daily_meal_request = daily_meal_request.filter(date__date__range=[date.today()-timedelta(days=7), date.today()])
        elif date_filter == 'MONTH':
            daily_meal_request = daily_meal_request.filter(date__date__range=[date.today()-timedelta(days=30), date.today()])
        elif date_filter == 'THIS-YEAR':
            daily_meal_request = daily_meal_request.filter(date__year=date.today().year)
    
    if request.user.is_staff:
        context = {
            'title': "Daily Meal Request",
            "daily_meal_request": daily_meal_request,
            "plan_names": set(daily_meal_request.values_list('plan__plan__name__name', flat=True).distinct()),
            "meal_types": set(daily_meal_request.values_list('meal__eating_type', flat=True).distinct()),
            "statuss": set(daily_meal_request.values_list('status', flat=True).distinct()),
            "date_filters": date_filters,
        }
        return render(request, 'meal/meal-request/list.html', context)
    
    elif user.is_cook:
        today = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()
        daily_meal_request = daily_meal_request.filter(
            status="Requested", 
            date__date = today
        ).order_by("date")
    context = {
        "daily_meal_request": daily_meal_request, 
        'title': "Meal to Cook",
        # "plan_names": daily_meal_request.values('plan__plan__name__name').distinct(),
        'today': today}
    
    # Counts
    plans = Plan.objects.filter(
        id__in= PlanPurchase.objects.filter(
            id__in = daily_meal_request.values_list('plan', flat=True)
        ).values_list('plan', flat=True))
    meals_count = []
    for plan in plans:
        meal_types = [i.strip() for i in plan.eating_type.split(",")]
        meal_type_counts = []
        for et in meal_types:
            qty = daily_meal_request.filter(meal__eating_type=et, plan__plan=plan).count()
            if qty > 0:
                d = {
                    "name": f"{plan.name} ({et})",
                    "quantity": qty
                }
                meal_type_counts.append(d)
        meals_count.append(meal_type_counts)
    context['meals_count'] = meals_count
    return render(request, 'meal/meal-request/list-cook.html', context)
    
    # elif user.is_delivery_person:
    #     daily_meal_request = MealRequestDaily.objects.select_related().filter(delivery_person=user)
    #     context = {"daily_meal_request": daily_meal_request, 'title': "Daily Meal Request"}
    #     return render(request, 'meal/meal-request/list-delivery-person.html', context)
    
            


def add_daily_meal(request):
    form = MealRequestForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            plan = PlanPurchase.objects.get(id=form.data['plan'])
            form.instance.requester = plan.user
            plan.remaining_meals = plan.remaining_meals + 1
            plan.save()
            form.save()
            return redirect('daily_meal_request_list')
    context = {
        "form": form,
        "title": "Add Daily Meal",
    }
    return render(request, 'meal/add_daily_meal.html', context)



""" 
Update Daily Meal Request
"""
def update_daily_meal(request, id):
    instance = get_object_or_404(MealRequestDaily, id=id)
    form = MealRequestUpdateForm(instance=instance)
    if request.method == 'POST':
        form = MealRequestUpdateForm(instance=instance, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_meal_request_list')
    context = {
        "form": form,
        "title": f"Update Daily Meal of {instance.requester}",
    }
    return render(request, 'meal/form.html', context)



def transaction_list(request):
    transaction = Transaction.objects.select_related().all()
    context = {"transaction": transaction, 'title': "Transaction List"}
    return render(request, 'user/transaction-list.html', context)



def update_delivery_person(request):
    if request.method == 'POST':
        meal_id = request.POST.get('meall')
        print(meal_id)
        delivery_person_id = request.POST.get('delivery_person_updatee')
        print(delivery_person_id)
        
        instance = get_object_or_404(MealRequestDaily, id=meal_id)
        
        if delivery_person_id:
            delivery_person = get_object_or_404(CustomUser, id=delivery_person_id)
            instance.delivery_person = delivery_person
        
        instance.save()

    return redirect("daily_meal_request_list")


def get_delivery_person_list_popup(request):
     #"""pop model using Ajax"""
    print("meal")
    meal_id = request.POST.get('meal_id')
    if request.method == 'POST':
        delivery_person = CustomUser.objects.filter(is_delivery_person=True, is_active=True)
        html = render_to_string("meal/delivery_boy_popup.html", {'delivery_person': delivery_person, 'meal_id': meal_id}, request=request)
        print(html)
        return JsonResponse({'update': html})



""" 
    Daily Meal Menu View
    Auther: Rajendra
"""

# Add Daily Meal Menu
def add_daily_meal_menu(request):
    form = DailyMealMenuForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('daily_meal_menu_list')
    context = {
        "form": form,
        "title": "Add Daily Meal Menu",
    }
    return render(request, 'meal/form.html', context)


# List of daily meal menu
def daily_meal_menu_list(request):
    context = {
        'title': "Daily Meal Menu List",
        "data": DailyMealMenu.objects.all().order_by('-date')
    }
    return render(request, 'meal/daily-meal-menu-list.html', context)


def daily_meal_menu_delete(request, id):
    instance = get_object_or_404(DailyMealMenu, id=id)
    instance.delete()
    return redirect('daily_meal_menu_list')


def daily_meal_menu_edit(request, id):
    instance = get_object_or_404(DailyMealMenu, id=id)
    form = DailyMealMenuForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('daily_meal_menu_list')
    context = {
        "title": "Update Daily Meal Menu",
        "form": form,
    }
    return render(request, 'meal/form.html', context)


""" Support Views. """

def supprt_list(request, id=None):
    context = {
        'title': "Customer Suport List",
        "helps": CustomerSupport.objects.all()
    }
    return render(request, 'support/list.html', context)



""" 
Home Page Banner view on App    
"""
# Add Banner
def add_banner(request):
    form = BannerForm(data=request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('banner_list')
    context = {
        "form": form,
        "title": "Add Banner",
    }
    return render(request, 'meal/form.html', context)


# List of Banners
def banner_list(request):
    context = {
        'title': "Banners List",
        "banners": Banner.objects.all()
    }
    return render(request, 'meal/banners.html', context)


def banner_delete(request, id):
    instance = get_object_or_404(Banner, id=id)
    instance.delete()
    return redirect('banner_list')


def banner_edit(request, id):
    instance = get_object_or_404(Banner, id=id)
    form = BannerForm(
        instance=instance, data=request.POST or None, files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('banner_list')
    context = {
        "title": "Update Banner",
        "form": form,
    }
    return render(request, 'meal/form.html', context)




""" 
Coupon Code Views    
"""
# Add coupon
def add_coupon(request):
    form = CouponForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    context = {
        "form": form,
        "title": "Add coupon",
    }
    return render(request, 'meal/form.html', context)


# List of coupons
def coupon_list(request):
    context = {
        'title': "Coupon List",
        "coupons": Coupan.objects.all()
    }
    return render(request, 'meal/coupons.html', context)


def coupon_delete(request, id):
    instance = get_object_or_404(Coupan, id=id)
    instance.delete()
    return redirect('coupon_list')


def coupon_edit(request, id):
    instance = get_object_or_404(Coupan, id=id)
    form = CouponForm(
        instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    context = {
        "title": "Update Coupon",
        "form": form,
    }
    return render(request, 'meal/form.html', context)




""" 
    Sales Connect view on App    
"""
# List of Sales Connect
def sales_connect_list(request):
    context = {
        'title': "Sales Connects List",
        "sales_connects": SalesConnect.objects.all()
    }
    return render(request, 'sales/sales_connects.html', context)


def sales_connect_delete(request, id):
    instance = get_object_or_404(SalesConnect, id=id)
    instance.delete()
    return redirect('sales_connect_list')


def sales_connect_edit(request, id):
    instance = get_object_or_404(SalesConnect, id=id)
    form = SalesConnectForm(
        instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('sales_connect_list')
    context = {
        "title": "Update Sales Connect",
        "form": form,
    }
    return render(request, 'meal/form.html', context)




""" 
    Block user to book the meal for purticular date and eating type entry view  
    Kitchen Off Views  
"""
# Add coupon
def add_kitchen_off(request):
    form = KitchenOffForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('kitchen_off_list')
    context = {
        "form": form,
        "title": "Add Kitchen Off Data",
    }
    return render(request, 'meal/form.html', context)


# List of Dates to Kitchen Off
def kitchen_off_list(request):
    context = {
        'title': "Kitchen Off List",
        "kitchen_offs": KitchenOffModel.objects.all()
    }
    return render(request, 'meal/kitchen_offs.html', context)


def kitchen_off_delete(request, id):
    instance = get_object_or_404(KitchenOffModel, id=id)
    instance.delete()
    return redirect('kitchen_off_list')


def kitchen_off_edit(request, id):
    instance = get_object_or_404(KitchenOffModel, id=id)
    form = KitchenOffForm(
        instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('kitchen_off_list')
    context = {
        "title": "Update Kitchen Off",
        "form": form,
    }
    return render(request, 'meal/form.html', context)



"""
Master Data of user  and meals are stored in database with following models
"""
@login_required
def master_data(request):
    users = User.objects.prefetch_related().filter(
        is_active=True, is_cook=False, is_staff=False)
    master_data = []
    all_purchese = PlanPurchase.objects.select_related("plan").filter(status=True)
    for user in users:
        user_purcheses = all_purchese.filter(user=user)
        
        if not user_purcheses.exists():
            continue
        
        user_data = {
            "email": user.email,
            "mobile_number": user.mobile_number,
            "name": user.name,
            
            "breakfast": {
                "purchese": user_purcheses.filter(plan__name__name__icontains="healthy").aggregate(Sum('total_meals'))['total_meals__sum'] or 0,
                "pending": user_purcheses.filter(plan__name__name__icontains="healthy").aggregate(Sum('remaining_meals'))['remaining_meals__sum'] or 0,
                "consumed": user_purcheses.filter(plan__name__name__icontains="healthy").aggregate(Sum('consumed_meals'))['consumed_meals__sum'] or 0,
            },
            "quick": {
                "purchese": user_purcheses.filter(plan__name__name__icontains="lite").aggregate(Sum('total_meals'))['total_meals__sum'] or 0,
                "pending": user_purcheses.filter(plan__name__name__icontains="lite").aggregate(Sum('remaining_meals'))['remaining_meals__sum'] or 0,
                "consumed": user_purcheses.filter(plan__name__name__icontains="lite").aggregate(Sum('consumed_meals'))['consumed_meals__sum'] or 0,
            },
            "regular": {
                "purchese": user_purcheses.filter(plan__name__name__icontains="regular").aggregate(Sum('total_meals'))['total_meals__sum'] or 0,
                "pending": user_purcheses.filter(plan__name__name__icontains="regular").aggregate(Sum('remaining_meals'))['remaining_meals__sum'] or 0,
                "consumed": user_purcheses.filter(plan__name__name__icontains="regular").aggregate(Sum('consumed_meals'))['consumed_meals__sum'] or 0,
            },
            "jumbo": {
                "purchese": user_purcheses.filter(plan__name__name__icontains="jumbo").aggregate(Sum('total_meals'))['total_meals__sum'] or 0,
                "pending": user_purcheses.filter(plan__name__name__icontains="jumbo").aggregate(Sum('remaining_meals'))['remaining_meals__sum'] or 0,
                "consumed": user_purcheses.filter(plan__name__name__icontains="jumbo").aggregate(Sum('consumed_meals'))['consumed_meals__sum'] or 0,
            },
            "premium": {
                "purchese": user_purcheses.filter(plan__name__name__icontains="premium").aggregate(Sum('total_meals'))['total_meals__sum'] or 0,
                "pending": user_purcheses.filter(plan__name__name__icontains="premium").aggregate(Sum('remaining_meals'))['remaining_meals__sum'] or 0,
                "consumed": user_purcheses.filter(plan__name__name__icontains="premium").aggregate(Sum('consumed_meals'))['consumed_meals__sum'] or 0,
            }
        }
        master_data.append(user_data)
    context = {"master_data": master_data, "title": "Master Data"}
    return render(request, 'meal/master-data.html', context)
