from django.db.models import Avg
from django.urls import reverse
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


# Category-model.......................................................
class Category(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )
    # parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to="images/")
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




# Category-model-end.......................................................

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, unique=True)
    logo = models.ImageField(upload_to="brand_logos/", null=True, blank=True)
    description = models.TextField(blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.name
    
# Product-model.......................................................

class Filter_Price(models.Model):
    
    FILTER_PRICE =(
        ('1000 TO 1000' , '1000 TO 1000'),
        ('1000 TO 2000' , '1000 TO 2000'),
        ('2000 TO 3000' , '2000 TO 3000'),
        ('3000 TO 4000' , '3000 TO 4000'),
        ('4000 TO 5000' , '4000 TO 5000'),
    )
    
    price = models.CharField(choices=FILTER_PRICE,max_length=60)


    
    def __str__(self):
        return self.price












class Product(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )
    VARIANTS = (
        ("None", "None"),
        ("Size", "Size"),
        ("Color", "Color"),
        ("Size-Color", "Size-Color"),
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )  # many to one relation with Category
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True) 
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to="images/", null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.IntegerField(default=0)
    detail = models.TextField()
    variant = models.CharField(max_length=130, choices=VARIANTS, default="None")
    minamount = models.IntegerField(default=3)
    filter_price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE,null=True)
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    def averageReview(self):
        reviews = Comment.objects.filter(product=self, status=True).aggregate(
            average=Avg("rate")
        )
        print(reviews)  # Add this line for debugging
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg


# Product-model-end.......................................................


# Image-model.......................................................
class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to="images/")

    def __str__(self):
        return self.title


# Image-model-end.......................................................


# Comment-model.......................................................
class Comment(models.Model):
    STATUS = (
        ("New", "New"),
        ("True", "True"),
        ("False", "False"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


# Comment-model-end.......................................................


# Color-model.......................................................
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe(
                '<p style="background-color:{}">Color </p>'.format(self.code)
            )
        else:
            return ""


# Color-model-end.......................................................


# Size-model.......................................................
class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


# Size-model-end.......................................................


# Variants-model.......................................................


class ImageTypes(models.Model):
    # product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,default=True)
    # variant = models.ForeignKey(Variants,on_delete=models.CASCADE,null=True,blank=True)
    image_id = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to="variantimages/")

    def __str__(self):
        return self.image_id


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image_types = models.ManyToManyField(ImageTypes, blank=True)

    def get_image_types(self):
        return self.image_types.all()

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


# Variants-model-end.......................................................
