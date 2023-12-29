from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from coupons.models import Coupon

from product.models import Product, Variants



#user-profile-model............................................
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=100)
    state = models.CharField(blank=True, max_length=50,null=True)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/users/')
    language = models.CharField(max_length=50, null=True, blank=True,default="English")
    banner_image = models.ImageField(blank=True,null=True,upload_to='images/users/')
    wallet = models.DecimalField(default=0, decimal_places=2, max_digits=10,null=True,blank=True)



    def __str__(self):
        return self.user.username

    
    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name 


    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return "No Image"
    image_tag.short_description = 'Image'
    
    
    
class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)    
    
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, null=True, default=None
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, null=True,blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, default=1)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"   
    


class Payementwallet(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    paymenttype=models.CharField(max_length=150,blank=True,null=True)
    wallet = models.DecimalField(default=0, decimal_places=2, max_digits=10,null=True,blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"PaymentWallet for User: {self.user}, Payment Type: {self.paymenttype}, Created on: {self.created}"



class ChatMessage(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    

    def __str__(self):
        return self.author.username
    
    def last_10_messages():
        return ChatMessage.objects.order_by('-timestamp').all()[:10]
    
    
    
    
    
     
#user-profile-model-end............................................
    