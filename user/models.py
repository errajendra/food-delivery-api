from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from .utils import *
from .managers import CustomUserManager



class BaseModel(models.Model):
    """abstract base model"""

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)



class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value



class CustomUser(AbstractUser):
    email = LowercaseEmailField(null=True, blank=True)
    mobile_number = models.CharField(
        _("Mobile Number"), max_length=100, validators=[phone_validator],
        unique=True
        
    )
    password = models.CharField(
        _("Password"), max_length=128, 
        help_text=_(
            "Use the same password for security reasons."),
    )
    name = models.CharField(
        _("Full Name"), max_length=100, validators=[name_validator], null=True, blank=True
    )
    otp = models.CharField(max_length=8, null=True, blank=True)
    image = models.ImageField(
        default="default.png",
        upload_to="user/image/",
        verbose_name="User Profile Image", null=True, blank=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_delivery_person = models.BooleanField(
        _("Delivery Person"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as Delivery Person. "
            "Unselect this instead of Delivery Person accounts has removed."
        ),
    )
    is_cook = models.BooleanField(
        _("Is Cook Person"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as Cook/Rasoiya Person. "
            "Unselect this instead of Cook/Rasoiya Person accounts has removed."
        ),
    )
    fcm_token = models.TextField(null=True, blank=True)
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
    
    def save(self, *args, **kwargs):
        """ This method is used to modify the password field
        converting text into hashed key"""
        if len(self.password) < 30:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



"""
    Notification Setting Table
"""
class NotificationSetting(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE,
        related_name="notification_setting",
        editable=False
    )
    push = models.BooleanField(default=True)
    email = models.BooleanField(default=True)
    def __str__(self) -> str:
        return str(self.user)



""" User Notification Model. """
class Notification(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='notifications')
    title = models.CharField(max_length=100)
    description = models.TextField()
    seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "%s - %s".format(self.user, self.title)



""" User Address Model """
class Address(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="address"
    )
    fullName = models.CharField("Name", max_length=50, null=True, blank=True)
    mobileNo = models.CharField("Mobile Number", max_length=15, null=True, blank=True)
    type = models.CharField(
        max_length=12, choices=[
            ("Home", "Home"),
            ("Office", "Office"),
            ("Other", "Other"),
        ],
        default = "Home"
    )
    house_number = models.CharField(
        verbose_name="House/Street Number",
        default="",
        max_length=30
    )
    address1 = models.CharField(
        verbose_name="Address 1",
        default="",
        max_length=50
    )
    address2 = models.CharField(
        verbose_name="Address 2",
        default="",
        max_length=50
    )
    city = models.CharField(
        verbose_name="City",
        max_length=50
    )
    state = models.CharField(
        verbose_name="State",
        max_length=50
    )
    zip = models.CharField(
        verbose_name="Zip/Pin Code",
        validators=[zip_validator],
        max_length=10
    )
    latitude = models.DecimalField(
        max_digits=16, decimal_places=10,
        null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=16, decimal_places=10,
        null=True, blank=True
    )
    def __str__(self):
        return str(self.id)

    @property
    def full_address(self):
        return "%s, %s %s %s, %s %s -%s" % (
            self.mobileNo,
            self.house_number, self.address1, self.address2,
            self.city, self.state, self.zip)



""" User Transaction Detail. """
class Transaction(BaseModel):
    
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"
    ABORTED = "Aborted"
    REFUNDED = "Refunded"
    
    PAYMENT_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (REFUNDED, "Refunded"),
        (ABORTED, "Aborted"),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    tracking_id = models.CharField(
        verbose_name="RazorPay Order ID",
        max_length=100, null=True, blank=True
    )
    razorpay_payment_id = models.CharField(
        verbose_name="RazorPay Payment ID",
        max_length=100, null=True, blank=True
    )
    razorpay_signature = models.CharField(
        verbose_name="RazorPay Signature ID",
        max_length=100, null=True, blank=True
    )
    bank_id = models.CharField(max_length=56, null=True, blank=True)
    card_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=12, choices=PAYMENT_STATUS_CHOICES,
        default=PENDING)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status_message = models.CharField(
        verbose_name="CC Avenue order status message",
        max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.user} - {self.amount} - {self.status}"
