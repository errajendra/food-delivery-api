from django.db import models
from meal.models import (
    MealRequestDaily as MealOrder
)
from user.models import (
    CustomUser as User,
    BaseModel, _
)



# Delivery Person Detail
# class DeliveryPerson(BaseModel):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE,
#         verbose_name="Delivery User"
#     )
#     full_address = models.TextField(null=True, blank=True)
#     status = models.BooleanField(
#         default=True,
#         help_text="Make it False it delivery Person has left the job."
#     )
    
#     class Meta:
#         verbose_name = "Delivery Person"
#         verbose_name_plural = "Delivery People"
        
#     def __str__(self):
#         return f'{self.user}'


# class MealDeliveryStatus(BaseModel):
#     meal_order = models.OneToOneField(
#         MealOrder,
#         on_delete=models.CASCADE,
#         related_name='delivery', 
#     )
#     delivery_person = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
#     status = models.CharField(
#         _("Delivery Status"),
#         choices=[
#             ("PENDING", "PENDING"),
#             ("ON DELIVERY", "ON DELIVERY"),
#             ("DELIVERED", "DELIVERED"),
#             ("UN DELIVERED", "UN DELIVERED"),
#         ],
#         default="PENDING"
#     )
    
#     class Meta:
#         verbose_name = 'Meal Delivery Status'
        
#     def __str__(self) -> str:
#         return f"{self.pk} - {self.status}"
