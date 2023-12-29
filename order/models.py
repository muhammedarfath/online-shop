from django.db import models
from django.contrib.auth.models import User
from coupons.models import Coupon
from product.models import Product, Variants
from user.models import UserProfile


# Cart..................................................
class CartView(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    coupons = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True
    )
    cart_item = models.ForeignKey(
        CartView, on_delete=models.CASCADE, null=True, default=None
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL, blank=True, null=True
    )  # relation with varinat
    quantity = models.IntegerField()
    single_price = models.FloatField(blank=True, null=True)

    def sub_total(self):
        return self.variant.price * self.quantity

    @property
    def price(self):
        if self.variant:  # Check if product exists
            return self.variant.price
        return 0  # or any default value you prefer

    @property
    def amount(self):
        if self.variant and self.variant.price:  # Check if product and its price exist
            return self.quantity * self.variant.price

        if self.coupons:
            return self.variant.price - self.coupons.discount_price


# Cart-ebd..................................................


# Order-product................................................


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_id



class Order(models.Model):
    ORDERSTATUS = (
    (1, "New"),
    (2, "Accepted"),
    (3, "Preparing"),
    (4, "OnShipping"),
    (5, "Completed"),
    (6, "Canceled"),
    (7, "Return"),
    )


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    order_number = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(blank=True, max_length=20)
    address_line1 = models.CharField(blank=True, max_length=1100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(blank=True, max_length=100)
    state = models.CharField(blank=True, max_length=20)
    order_total = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    status = models.IntegerField(choices=ORDERSTATUS, default=1,blank=True,null=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    user_product_status = models.CharField(blank=True, max_length=100)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Return", "Return"),
        ("Canceled", "Canceled"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField()
    price = models.FloatField()
    grand_total = models.FloatField(blank=True, null=True)
    ordered = models.BooleanField(default=False, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user_note = models.CharField(blank=True, max_length=100)


# Order-product-end................................................
