from django.contrib import admin
from .models import Brand, Category, Color, Comment, ImageTypes,Product,Images, Size, Variants,Filter_Price
import admin_thumbnails
# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
    prepopulated_fields={'slug':('title',)}
   
   
   
class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True   
   
   
@admin_thumbnails.thumbnail('image')   
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

    


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','product','rate','id')



class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline,ProductVariantsInline]
    prepopulated_fields={'slug':('title',)}
    
@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','id','image_thumbnail']    
 
 
@admin_thumbnails.thumbnail('image')
class VariantImages(admin.ModelAdmin):
    list_display = ['image','title','id','image_thumbnail'] 
    # inlines = [VariantImageInline]    
 

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']


admin.site.register(Brand)        
admin.site.register(ImageTypes,VariantImages)    
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(Filter_Price)