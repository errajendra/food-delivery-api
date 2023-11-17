from django.shortcuts import render
from user.models import CustomUser
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.



def delivery_person_list(request):
    delivery_person = CustomUser.objects.filter(is_delivery_person=True, is_active=True)
    context = {"delivery_person": delivery_person, 'title': "Delivery Person List"}
    return render(request, 'delivery/delivery-person-list.html', context)


from django.shortcuts import render, redirect
from user.models import CustomUser
from .forms import DeliveryPersonForm

def add_delivery_person(request):
    form = DeliveryPersonForm(request.POST or None)

    if request.method == 'POST':
        email = form.data.get("email")  # Get the email directly from the form data

        # Check if the email already exists
        existing_user = CustomUser.objects.filter(email=email).first()

        if existing_user:
            # Update the existing user's information without changing the email
            existing_user.name = form.data.get("name")
            existing_user.mobile_number = form.data.get("mobile_number")
            existing_user.set_password(form.data.get("password"))
            existing_user.is_delivery_person = True
            existing_user.save()
        else:
            # If no existing user, create a new user
            user = form.save(commit=False)
            user.is_active = True
            user.is_delivery_person = True
            user.save()

        return redirect("delivery_person_list")
    
    return render(
        request,
        "delivery/add_delivery_person.html",
        {"form": form, 'title': "Add Delivery Person User"}
    )

    
def delete_delivery_person(request,id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_delivery_person = False
    user.save()
    return redirect('delivery_person_list') 



