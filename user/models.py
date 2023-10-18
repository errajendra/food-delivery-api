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
    email = LowercaseEmailField(unique=True)
    mobile_number = models.CharField(
        _("Mobile Number"), max_length=100, validators=[phone_validator],
        null=True, blank=True
    )
    password = models.CharField(
        _("Password"), max_length=128, validators=[password_validator]
    )
    name = models.CharField(
        _("Full Name"), max_length=100, validators=[name_validator]
    )
    otp = models.CharField(max_length=8, null=True, blank=True)
    image = models.ImageField(
        default="default.png",
        upload_to="user/image/",
        verbose_name="User Profile Image",
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ('name',)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.name)+" - "+str(self.mobile_number)
    
    @property
    def wallet_amount(self):
        amount = self.wallet.filter(
            status="Success"
        ).aggregate(models.Sum('coins'))['coins__sum']
        if amount:
            return amount
        return 0.00
    
    def save(self, *args, **kwargs):
        """ This method is used to modify the password field
        converting text into hashed key"""
        if len(self.password) < 30:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



"""
    Wallete or Coin Table
"""
class Wallet(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name="wallet"
    )
    t_type = models.CharField(
        verbose_name="Transaction Type",
        choices=[("Credit", "Credit"), ("Debit", "Debit")],
        max_length=6
    )
    coin_type = models.CharField(
        verbose_name="Coin Type",
        choices=[("GOLD", "GOLD"), ("SILVER", "SILVER")],
        max_length=6
    )
    coins = models.FloatField(
        help_text="Use positive number for Credit and negative number for Debit"
    )
    status = models.CharField(
        choices=[
            ("Pending", "Pending"),
            ("Success", "Success"),
            ("Failed", "Failed"),
        ],
        max_length=10,
        default = "Success"
    )
    remark = models.CharField(
        max_length=50,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.user)+" > "+str(self.coins)

    class Meta:
        ordering = ('-created_at',)



"""
    Notification Setting Table
"""
class NotificationSetting(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE,
        related_name="notification_setting"
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
