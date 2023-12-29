from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('delete_cart_item/<int:id>', views.delete_cart_item, name='delete_cart_item'),
    path("shopcart/", views.shopcart, name="shopcart"),
    path("orderproduct/", views.orderproduct, name="orderproduct"),
    # path('proceed-to-pay/', OrderViews.razorpaycheck, name='razorpaycheck'),
    path("checkout/", views.checkout, name="checkout"),
    # path("update_quantity/", views.update_quantity, name="update_quantity"),
    path("payments/", views.payments, name="payments"),
    path("apply_coupon/",views.apply_coupon,name="apply_coupon"),
    path("order_complete/", views.order_complete, name="order_complete"),
    path("cash_on_delivery/<int:number>", views.cash_on_delivery, name="cash_on_delivery"),
    path("wallet_payment/<int:number>", views.wallet_payment, name="wallet_payment"),
    path("success/", views.success, name="success"),
]
