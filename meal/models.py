from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from PIL import Image
from user.models import (
    BaseModel, CustomUser as User,
    Transaction, _
)



""" Meal Type Model."""
class MealType(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="""
            Meal Type like: Regular, Jumbo
        """
    )
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


"""
Plan Detail Model
"""
class Plan(BaseModel):
    name = models.ForeignKey(
        MealType, on_delete=models.CASCADE, related_name="plans",
        verbose_name="Plan Name", help_text = "Select Plan Type"
    )
    price = models.FloatField(verbose_name="Price of Plan")
    number_of_meals = models.PositiveIntegerField(verbose_name="Number of Meals")
    # saving_per_day = models.FloatField("Per Day Saving Price", default=0)
    tag = models.CharField(
        verbose_name="Select- Recommended/Most Popular",
        choices=(('Recommended', 'Recommended'), ('Most Popular', 'Most Popular')),
        max_length=20,
        default="Most Popular"
    )
    eating_type = models.CharField(
        verbose_name = "Eating Type",
        default = 'Lunch',
        max_length = 50)
    # items = RichTextField(null=True, blank=True)
    # benifits = RichTextField(null=True, blank=True)
    validity = models.PositiveIntegerField(
        verbose_name = "Validity in Days", default=180)
    
    def __str__(self):
        return str(self.name) + " -> " + str(self.number_of_meals)
    
    @property
    def price_per_meal(self):
        return round(float(self.price)/self.number_of_meals, 2)
    
    class Meta:
        unique_together = ('name', 'number_of_meals')
        ordering = ['name']



"""
Plan Purchage Detail Model
"""
class PlanPurchase(BaseModel):
    plan = models.ForeignKey(
        Plan,
        related_name = 'planpurchases',
        on_delete = models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name = 'userplans',
        on_delete = models.CASCADE
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE
    )
    total_meals = models.PositiveIntegerField(
        verbose_name = "Total Number of Meals Piurchese",
        help_text = "It will set automaticaly to purchase plan meal number."
    )
    remaining_meals = models.PositiveIntegerField(
        verbose_name = "Number of Meals Remaining",
        help_text = "It will update automaticaly when order is created or canceled."
    )
    status = models.BooleanField(
        default = False,
        help_text =_(
            "Plan Purchese Status"
            "Make it True for Successfuly Purchese and"
            "False if not purchesd yet."
        )
    )
    # address = models.CharField(
    #     max_length=255, verbose_name="User Address to Deliver Meal",
    #     null = True, blank = True
    # )

    def __str__(self):
        return f"{self.user} - {self.plan.name}"



"""
Meal/Food/Lunch/Denner Model
"""
class Meal(BaseModel):
    name = models.CharField(
        max_length=100, verbose_name="Meal Name",
        help_text="With Rice/Without Rice")
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, help_text="Meal Items")
    eating_type = models.CharField(
        verbose_name="Eating Type",
        choices=[
            ('Breakfast', 'Breakfast'), 
            ('Lunch', 'Lunch'),
            ('Dinner', 'Dinner')
        ],
        default='Lunch',
        max_length=10)
    image = models.ImageField(upload_to="meals", blank=True)
    
    class Meta:
        unique_together = ('name', 'meal_type', 'eating_type')
    
    def __str__(self):
        return f"{self.meal_type} ({self.eating_type})"
    



""" Menu Meal list.
 select date and meal menu for that perticular date.
"""
class DailyMealMenu(BaseModel):
    date = models.DateField()
    meal_type = models.ForeignKey(
        MealType, on_delete=models.CASCADE,
        related_name="menu_for_dates")
    eating_type = models.CharField(
        verbose_name="Eating Type",
        choices=[
            ('Breakfast', 'Breakfast'), 
            ('Lunch', 'Lunch'),
            ('Dinner', 'Dinner')
        ],
        max_length=10)
    items = RichTextField(help_text="Meal Menu Items")
    
    class Meta:
        unique_together = ('date', 'meal_type', 'eating_type')
    
    def __str__(self) -> str:
        return str(self.date)



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
    
    mobile_number = models.CharField("Mobile Number", max_length=15, null=True, blank=True)
    address = models.CharField(
        max_length=255, verbose_name="User Address to Deliver Meal",
        null = True, blank = True
    )
    latitude = models.DecimalField(
        max_digits=16, decimal_places=10,
        null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=16, decimal_places=10,
        null=True, blank=True
    )
    
    instruction = models.CharField(
        verbose_name = "Customer Instruction", max_length = 100, 
        null = True, blank = True)
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
            ('Success', 'Success'), # Confirm
            ('Requested', 'Requested'),
            ('Prepared', 'Prepared'), 
            ('Packed', 'Packed'),
            ('Delivered', 'Delivered'),
        ),
        max_length=20,
        default="Requested"
    )
    

    def __str__(self) -> str:
        return str(self.requester) + " - "+ str(self.meal)

    class Meta:
        ordering = ['-date']
        
    def meal_items(self):
        menus = DailyMealMenu.objects.filter(
            date = self.date.date(),
            eating_type = self.meal.eating_type,
            meal_type = self.meal.meal_type
        )
        if menus:
            return menus.first().items
        return " "



""" 
    Customer Support Model Table
"""
class CustomerSupport(BaseModel):
    user = models.ForeignKey(
        User,
        related_name='help_raised',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=(
            ('Requested', 'Requested'), 
            ('Under Review', 'Under Review'),
            ('Close', 'Close'),
            ('Rejected', 'Rejected'),
        ),
        max_length=20,
        default="Requested"
    )
    attachment = models.FileField(upload_to='support/attachments/', blank=True)
    message = models.TextField()

    @property
    def can_be_closed(self):
        """ Returns True if this support ticket can be closed (i.e., has been resolved), False otherwise."""
        return self.status in ['Under Review', 'Rejected']

    def close(self):
        """ Close this support ticket by setting its status to Under Review and saving it."""
        assert self.can_be_closed, f'Cannot close ticket with status "{self .status}"!'
        self.status = "Close"
        self.save()



""" 
Home Page banner image.
"""
def banner_image_size(image):
    # def validator(image):
    width = 720
    height = 300
    img = Image.open(image)
    fw, fh = img.size
    if not fw == width or not fh == height:
        raise ValidationError(
            f"Height {height} or Width {width} is not found.")
    

class Banner(BaseModel):
    
    image = models.ImageField(
        upload_to='banners/',
        validators=[banner_image_size],
        help_text="Height 300 and Width 720 is only allowed."
    )
    alt = models.CharField(max_length=255)
    status = models.BooleanField(
        default=True,
        help_text=(
            "Status is True it means it will show in listing.",
            "Uncheck this for removing this entry from listing."
        ))



class SalesConnect(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_connects")
    employee_id = models.CharField(_("Employee ID"), max_length = 50)
    status = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.employee_id)
