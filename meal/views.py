from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import (
    CategoryForm, Category,
    SubCategory, SubCategoryForm,
    Meal, MealForm,
    Plan, PlanForm, MealRequestForm,
    DailyMealMenuForm
)
from .models import *
from user.models import *
from django.template.loader import render_to_string
from django.http import JsonResponse



"""
    Category View Functions
"""
def category_add(request):
    # Add Category Method
    form = CategoryForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('category_list')
    context = {
        "form": form,
        "title": "Add Category Form",
    }
    return render(request, 'meal/form.html', context)


def category_list(request):
    # List Categories Method
    categories = Category.objects.all().order_by("name")
    context = {"categories": categories, 'title': "Categories"}
    return render(request, 'meal/categories.html', context)


def category_edit(request, id):
    # Edit Category Method
    instance = get_object_or_404(Category, id=id)
    form = CategoryForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('category_list')
    context = {
        "title": "Update Category",
        "form": form,
    }
    return render(request, 'meal/form.html', context)



"""
    Sub Category View Functions
"""
def subcategory_add(request):
    # Add Category Method
    form = SubCategoryForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('subcategory_list')
    context = {
        "form": form,
        "title": "Add Sub Category Form",
    }
    return render(request, 'meal/form.html', context)


def subcategory_list(request):
    # List Categories Method
    categories = SubCategory.objects.select_related().all().order_by("name")
    context = {"categories": categories, 'title': "Sub Categories"}
    return render(request, 'meal/sub-categories.html', context)


def subcategory_edit(request, id):
    # Edit Category Method
    instance = get_object_or_404(SubCategory, id=id)
    form = SubCategoryForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('subcategory_list')
    context = {
        "title": "Update Sub Category",
        "form": form,
    }
    return render(request, 'meal/form.html', context)



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


def plan_purchase_list(request):
    plan_purchase = PlanPurchase.objects.select_related().all()
    context = {"plan_purchase": plan_purchase, 'title': "Plan Purchase List"}
    return render(request, 'meal/plan-purchase-list.html', context)

def daily_meal_request_list(request):
    user = request.user
    if request.user.is_staff:
        daily_meal_request = MealRequestDaily.objects.select_related().all()
        context = {"daily_meal_request": daily_meal_request, 'title': "Daily Meal Request"}
        return render(request, 'meal/daily-meal-request.html', context)
    else:
        daily_meal_request = MealRequestDaily.objects.select_related().filter(delivery_person=user)
        context = {"daily_meal_request": daily_meal_request, 'title': "Daily Meal Request"}
        return render(request, 'meal/daily-meal-request-delivery-person.html', context)
    
            


def add_daily_meal(request):
    form = MealRequestForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('daily_meal_request_list')
    context = {
        "form": form,
        "title": "Add Daily Meal",
    }
    return render(request, 'meal/add_daily_meal.html', context)



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
