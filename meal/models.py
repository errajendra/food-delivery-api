from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from user.models import (
    BaseModel, CustomUser as User,
    Transaction,
)



""" Meal Categories Model."""
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="""
            Meal Category Like- Cuisine, Portion Size etc
        """
    )
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100,
        help_text="Sub Category of Cateory"
    )
    description = models.TextField()

    
    def __str__(self) -> str:
        return self.category.name+" > "+self.name


"""
Meal/Food/Lunch/Denner Model
"""
class Meal(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Meal Name")
    description = models.CharField(max_length=250)
    price = models.FloatField(verbose_name="Starting Price/Day")
    eating_type = models.CharField(
        verbose_name="Eating Type",
        choices=[
            ('Breakfast', 'Breakfast'), 
            ('Lunch', 'Lunch'),
            ('Dinner', 'Dinner')
        ],
        default='Lunch',
        max_length=10)
    # category = models.ForeignKey(
    #     Category, on_delete=models.SET_NULL,
    #     null=True, blank=True
    # )
    # sub_category = models.ForeignKey(
    #     SubCategory, on_delete=models.SET_NULL,
    #     null=True, blank=True
    # )
    image = models.ImageField(upload_to="meals", blank=True)
    
    def __str__(self):
        return self.name
    


"""
Plan Detail Model
"""
class Plan(BaseModel):
    name = models.CharField(
        verbose_name="Plan Name", max_length=100
    )
    price = models.FloatField(verbose_name="Plan Price")
    duration = models.PositiveIntegerField(verbose_name="Number of Meals")
    # saving_per_day = models.FloatField("Per Day Saving Price", default=0)
    tag = models.CharField(
        verbose_name="Select- Recommended/Most Popular",
        choices=(('Recommended', 'Recommended'), ('Most Popular', 'Most Popular')),
        max_length=20,
        default="Most Popular"
    )
    eating_type = models.CharField(
        verbose_name="Eating Type",
       
        default='Lunch',
        max_length=50)
    items = RichTextField(null=True, blank=True)
    benifits = RichTextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def price_per_meal(self):
        return round(self.price / self.duration, 2)



"""
Plan Purchage Detail Model
"""
class PlanPurchase(BaseModel):
    plan = models.ForeignKey(
        Plan,
        related_name='planpurchases',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='userplans',
        on_delete=models.CASCADE
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE
    )
    remaining_meals = models.PositiveIntegerField(
        verbose_name="Number of Meals Remaining",
        help_text="It will set automaticaly to purchase plan meal number."
    )
    status = models.BooleanField(
        default=False,
        help_text="""
            Plan Purchese Status,
            Make it True for Successfuly Purchese and
            False if not purchesd yet.
        """
    )
    address = models.CharField(
        max_length=255, verbose_name="User Address to Deliver Meal",
    )

    def __str__(self):
        return f"{self.plan.name}"



""""
    Meal (Menu) Daily Request base on purhese plan. 
    Select Menu Option Daily.
"""
class MealRequestDaily(BaseModel):
    requester = models.ForeignKey(
        User,
        related_name='requested_meals',
        on_delete=models.CASCADE,
    )
    plan = models.ForeignKey(
        PlanPurchase,
        related_name='requested_meals',
        on_delete=models.CASCADE,
        limit_choices_to={
            'status': True,
            'remaining_meals__gt' : 0
        }
    )
    meal = models.ForeignKey(
        Meal, related_name="requested_meals",
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(default=timezone.now)
    delivery_person = models.ForeignKey(
        User,
        related_name='delivery',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={
            "is_delivery_person":True
        }
    )
    status = models.CharField(
        choices=(
            ('Success', 'Success'),
            ('Requested', 'Requested'), 
            ('Cancelled', 'Cancelled')
        ),
        max_length=20,
        default="Requested"
    )
    

    def __str__(self) -> str:
        return str(self.requester) + " - "+ str(self.meal)

    class Meta:
        ordering = ['-date']
