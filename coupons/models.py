from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    offer_name = models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=50, unique=True)
    image = models.ImageField(blank=True, upload_to="images/",null=True)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    expiration_time = models.DateTimeField(default=timezone.localtime) 
    active = models.BooleanField(default=True)
    is_one_time_use = models.BooleanField(default=False) 
    