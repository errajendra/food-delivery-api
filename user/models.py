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
    house_number = models.CharField(
        verbose_name="House/Street Number",
        default="",
        max_length=20
    )
    address1 = models.CharField(
        verbose_name="Address 1",
        default="",
        max_length=36
    )
    address2 = models.CharField(
        verbose_name="Address 2",
        default="",
        max_length=36
    )
    city = models.CharField(
        verbose_name="City",
        max_length=36
    )
    state = models.CharField(
        verbose_name="State",
        max_length=20
    )
    zip = models.CharField(
        verbose_name="Zip/Pin Code",
        validators=[zip_validator]
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
        return self.user

    @property
    def full_address(self):
        return "%s %s %s, %s %s -%s" % (
            self.house_number, self.address1, self.address2,
            self.city, self.state, self.zip)
