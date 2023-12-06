from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.

# class User(AbstractUser):
#     phone_number = models.CharField(max_length=10,unique=True)
#     is_phone_verified = models.BooleanField(default=False)

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []
#     objects = UserManager()

class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True)
    is_phone_verified = models.BooleanField(default=False)

    objects = UserManager()

    # Specify unique related_name values for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
    
class UserPersonalInfo(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length = 50)
    dob = models.CharField(max_length=10)
    emailid = models.EmailField()
    marital_status = models.CharField(max_length=10)
    mother_name = models.CharField(max_length = 50)
    address_landmark = models.CharField(max_length = 50)
    address_city = models.CharField(max_length = 50)
    address_state = models.CharField(max_length=50)
    address_pincode = models.CharField(max_length = 10)
    loan_type = models.CharField(max_length=15)
    pancard = models.CharField(max_length=30)
    aadhar = models.CharField(max_length=30)
    loan_amount = models.CharField(max_length = 10)
    deposite_period = models.CharField(max_length=5)
    itr = models.CharField(max_length=15,default="")
    turnover = models.CharField(max_length=10,default="")
    gstno = models.CharField(max_length=25,default="")
    bank_name = models.CharField(max_length=20)
    account_number = models.CharField(max_length=25)
    ifsc_code = models.CharField(max_length = 20)
    branch_name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_id.username})"


class Otp(models.Model):
    phone_number = models.CharField(max_length=10,unique=True)
    otp = models.CharField(max_length=4)
    created_at = models.TimeField( auto_now_add=True)       
    class Meta:
        db_table = 'pp_otp' 
