from django.contrib import admin

# Register your models here.
from user.models import Payementwallet, UserProfile, WishlistItem,ChatMessage

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','address', 'phone','city','country','image_tag']

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(WishlistItem)
admin.site.register(Payementwallet)
admin.site.register(ChatMessage)