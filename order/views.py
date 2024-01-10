import decimal
import json

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from coupons.models import Coupon
from home.models import Setting
from user.models import Payementwallet, UserProfile, WishlistItem
from .models import CartView, Order, OrderProduct, ShopCart, Payment
from django.contrib import messages
from product.models import Category, Comment, Product, Variants
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import random
from django.utils import timezone
from decimal import Decimal
import datetime
from datetime import date
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Order Page")


# cart-function..................................................
def _cart_id(request):  # private function
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def addtoshopcart(request, id):
    current_user = request.user
    product = Product.objects.get(pk=id)


    if current_user.is_authenticated:
        try:
            wishitem = WishlistItem.objects.get(user=current_user, product=product)
            wishitem.delete()
        except WishlistItem.DoesNotExist:
            pass 
        if product.variant != "None":
            variantid = request.POST.get("variantid")
            checkinvariant = ShopCart.objects.filter(
                variant=variantid, user=current_user
            )
            if checkinvariant:
                control = 1
            else:
                control = 0
        else:
            checkinproduct = ShopCart.objects.filter(product=id, user=current_user)
            if checkinproduct:
                control = 1
            else:
                control = 0

        if control == 1:
            if product.variant == "None":
                data = ShopCart.objects.get(product=id, user=current_user)
            else:
                data = ShopCart.objects.get(
                    product=id, user=current_user, variant=variantid
                )
            data.quantity += 1  # Increment the quantity if the item already exists
            data.save()
        else:
            product = get_object_or_404(Product, id=id)
            variant = get_object_or_404(Variants, id=variantid)
            data = ShopCart()
            data.product = product
            data.variant = variant
            data.user = current_user
            data.quantity = 1
            data.single_price = variant.price
            data.save()

        return HttpResponseRedirect("/order/shopcart/")

    else:
        try:
            cart = CartView.objects.get(
                cart_id=_cart_id(request),
            )
        except CartView.DoesNotExist:
            cart = CartView.objects.create(cart_id=_cart_id(request))

        cart.save()

        if product.variant != "None":
            variantid = request.POST.get("variantid")
            checkinvariant = ShopCart.objects.filter(variant=variantid, cart_item=cart)
            if checkinvariant:
                control = 1
            else:
                control = 0
        else:
            checkinproduct = ShopCart.objects.filter(product=id, cart_item=cart)
            if checkinproduct:
                control = 1
            else:
                control = 0

        if control == 1:
            if product.variant == "None":
                data = ShopCart.objects.get(product=id, cart_item=cart)
            else:
                data = ShopCart.objects.get(
                    product=id, cart_item=cart, variant=variantid
                )
            data.quantity += 1  # Increment the quantity if the item already exists
            data.save()
        else:
            product = get_object_or_404(Product, id=id)
            variant = get_object_or_404(Variants, id=variantid)
            data = ShopCart()
            data.product = product
            data.variant = variant
            data.cart_item = cart
            data.quantity = 1
            data.single_price = variant.price
            data.save()

        return HttpResponseRedirect("/order/shopcart/")


def update_quantity(request):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        product = int(request.POST.get("product_id"))
        action = request.POST.get("action")
        product_qty = int(request.POST.get("quantity", 0))
        if request.user.is_authenticated:
            cart_item = get_object_or_404(ShopCart, user=request.user, variant=product)
        else:
            cart = CartView.objects.get(cart_id=_cart_id(request))
            cart_item = get_object_or_404(ShopCart,cart_item=cart,variant=product)
                

        if product_qty == 0:
            return JsonResponse({"status": "Zero quantity not allowed"})

        if product_qty > cart_item.variant.quantity:
            return JsonResponse(
                {"status": "Requested quantity exceeds available quantity"}
            )

        cart_item.quantity = product_qty
        cart_item.save()

        try:
            if request.user.is_authenticated:
                cart_items = ShopCart.objects.filter(user=request.user)
            else:
                cart = CartView.objects.get(cart_id=_cart_id(request))
                cart_items = ShopCart.objects.filter(cart_item=cart)

            total = sum(cart_item.variant.price * item.quantity for item in cart_items)
            tax = (2 * total) / 100
            shipping = 40
            grand_total = total + tax
            
            

            product_price = cart_item.variant.price
            single_price = product_price * cart_item.quantity
            cart_item.single_price = single_price  # Update single_price in the model
            cart_item.save()
            
            return JsonResponse(
                {
                    'status':"success",
                    "single_price": single_price,
                    "grand_total": grand_total,
                    "tax": tax,
                    "shipping": shipping,
                    'total':total
                }
            )
        except ObjectDoesNotExist:
            pass
    return JsonResponse({"status": "Invalid requst method"})


def shopcart(request, cart_items=None, total=0, quantity=0):
    try:
        if request.user.is_authenticated:
            cart_items = ShopCart.objects.filter(user=request.user)
        else:
            cart = CartView.objects.get(cart_id=_cart_id(request))
            cart_items = ShopCart.objects.filter(cart_item=cart)

        for cart_item in cart_items:
            if cart_item.variant:  # Check if product exists
                total += cart_item.variant.price * cart_item.quantity
                quantity += cart_item.quantity
        # product_comments = Comment.objects.filter(product=cart_item.product)      
    except ObjectDoesNotExist:
        pass
    shipping = 40
    tax = (2 * total) / 100
    grand_total = total + tax
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "shipping": shipping,
        "grand_total": grand_total,
        "tax": tax,
        # "product_comments":product_comments
    }

    return render(request, "shopcart_product.html", context)


def counter(request):
    cart_count = 0
    wallet = None  
    try:
        if request.user.is_authenticated:
            cart_item = ShopCart.objects.filter(user=request.user)
            userp = get_object_or_404(UserProfile,user=request.user)
            wallet = userp.wallet
        
        else:
            cart_item = ShopCart.objects.filter(
                cart_item=CartView.objects.get(cart_id=_cart_id(request))
            )
        for item in cart_item:
            cart_count += (
                item.quantity
            )  # Adjust this line based on your actual field structure
    except CartView.DoesNotExist:
        cart_count = 0
        

    return {"cart_count": cart_count,"wallet":wallet}




def delete_cart_item(request, id):
    variant = get_object_or_404(Variants, id=id)
    if request.user.is_authenticated:
        cart_item = ShopCart.objects.get(variant=variant, user=request.user)
    else:
        cart = CartView.objects.get(cart_id=_cart_id(request))
        cart_item = ShopCart.objects.get(variant=variant, cart_item=cart)
    messages.info(request, "Are you sure , You want to delete this item?")
    cart_item.delete()
    return HttpResponseRedirect("/order/shopcart/")


# cart-function-end..................................................


# Order-Product........................................................
@login_required(login_url="/user/login/") 
def orderproduct(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    coupon = Coupon.objects.all()
    if request.user.is_authenticated:
        cart_items = ShopCart.objects.filter(user=request.user)
    else:
        cart_user = CartView.objects.get(cart_id=_cart_id(request))
        cart_items = ShopCart.objects.filter(cart_item=cart_user)
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return HttpResponseRedirect("/shopcart/")

    userprofile = get_object_or_404(UserProfile,user=request.user)
    for cartitem in cart_items:
        total += cartitem.variant.price * cartitem.quantity
        quantity += cartitem.quantity
    shipping = 40
    tax = (2 * total) / 100
    grand_total = total + tax
    context = {
        "cart_items": cart_items,
        "grand_total": grand_total,
        "quantity": quantity,
        "userprofile": userprofile,
        "coupon": coupon,
        "shipping": shipping,
        "tax": tax,
    }
    return render(request, "order_form.html", context)


# Order-Product-end........................................................
def checkout(request, total=0, quantity=0):
    url = request.META.get("HTTP_REFERER")
    current_user = request.user

    cart_items = ShopCart.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return HttpResponseRedirect("/order/shopcart/")

    grand_total = 0
    tax = 0
    for cartitem in cart_items:
        total += cartitem.variant.price * cartitem.quantity
        quantity += cartitem.quantity

    shipping = 40
    tax = (2 * total) / 100
    grand_total = total + tax
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address_line1 = request.POST.get("address_line1")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        if (
            not first_name
            or not phone
            or not email
            or not address_line1
            or not state
            or not city
            or not country
        ):
            messages.error(request, "fields cannot empty")
            return HttpResponseRedirect(url)
        data = Order()
        data.user = current_user
        data.first_name = first_name
        data.phone = phone
        data.email = email
        data.address_line1 = address_line1
        data.country = country
        data.state = state
        data.city = city
        data.tax = tax
        data.order_total = grand_total
        data.ip = request.META.get("REMOTE_ADDR")
        data.save()
        # genreate order number
        yr = int(datetime.date.today().strftime("%y"))
        dt = int(datetime.date.today().strftime("%d"))
        mt = int(datetime.date.today().strftime("%m"))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%y%m%d")
        order_number = current_date + str(d.day)
        data.order_number = order_number
        data.save()

        order = Order.objects.filter(
            user=request.user, is_ordered=False, order_number=order_number
        )
        if order.exists():
            order = order.last()
        else:
            pass
    
        context = {
            "order": order,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total,
            "shipping": shipping,
            "total":total
        }
        return render(request, "payment.html", context)
    else:
        messages.error(
            request, "There was an error with your order. Please check the form."
        )
        return HttpResponseRedirect("/order/checkout/")
    
@login_required
def apply_coupon(request, total=0, quantity=0):
    if request.method == "POST":
        user = request.user
        cart_items = ShopCart.objects.filter(user=user)
        grand_total = 0
        tax = 0

        for cartitem in cart_items:
            total += cartitem.variant.price * cartitem.quantity
            quantity += cartitem.quantity

        shipping = 40
        tax = (2 * total) / 100
        grand_total = total + tax

        coupon_code = request.POST.get('coupon')

        # Fetch the coupon from the database
        coupon = Coupon.objects.filter(code=coupon_code, active=True).first()

        if coupon:
            # Check if the coupon is valid (not expired)
            current_time = timezone.now()
            if current_time <= coupon.expiration_time:

                # Check if the user has used the coupon before
                if Order.objects.filter(user=user, coupon=coupon, is_ordered=True).exists():
                    return JsonResponse({'error': 'You have already used this coupon.'})

                orders = Order.objects.filter(user=user, is_ordered=False)

                if orders.exists():
                    # Use the latest order if there are multiple orders
                    order = orders.latest('create_at')
                else:
                    # Create a new order if no existing orders
                    order = Order.objects.create(user=user, total_amount=0)

                # Check if the order total meets the minimum amount requirement
                if total >= coupon.minimum_amount:
                    # Apply the discount to the total
                    discount_amount = total - coupon.discount_price
                    grand_total = discount_amount + tax

                    order.coupon = coupon
                    order.save()

                    # Update the cart items with the new prices
                    for cart_item in cart_items:
                        cart_item.variant.price = grand_total

                    # Return a JsonResponse with updated values
                    response_data = {
                        'total': total,
                        'coupon': discount_amount,
                        'tax': tax,
                        'shipping': shipping,
                        'grand_total': grand_total,
                        'success': f"Coupon '{coupon.offer_name}' applied successfully! You saved ₹{coupon.discount_price:.2f}",
                    }
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({'error': f"The order total must be greater than or equal to ₹{coupon.minimum_amount} to use this coupon."})
            else:
                return JsonResponse({'error': 'Invalid coupon or expired'})
        else:
            return JsonResponse({'error': 'Invalid coupon code'})

    return JsonResponse({'error': 'Invalid request method'})



def payments(request):
    body = json.loads(request.body)
    orders = Order.objects.filter(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )
    if orders.exists():
        order = (
            orders.last()
        )  # You may want to add additional logic if there are multiple matching orders
        
        coupon_discount = 0 

        # Check if the order has a coupon applied
        if order.coupon:
            coupon_discount = order.coupon.discount_price
        payment = Payment(
            user=request.user,
            payment_id=body["transID"],
            payment_method=body["payment_method"],
            amount_paid=order.order_total - coupon_discount,
            status=body["status"],
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_item = ShopCart.objects.filter(user=request.user)
        for item in cart_item:
            orderproduct = OrderProduct()
            orderproduct.order = order
            orderproduct.payment = payment
            orderproduct.user = request.user
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            orderproduct.variant = item.variant
            orderproduct.price = item.variant.price
            orderproduct.grand_total = order.order_total - coupon_discount
            orderproduct.ordered = True
            orderproduct.save()

            variant = Variants.objects.get(id=item.variant.id)
            variant.quantity -= item.quantity
            variant.save()

        ShopCart.objects.filter(user=request.user).delete()
        mail_subject = "Thank you for your order"
        message = render_to_string(
            "order_recieved_email.html", {"user": request.user, "order": order}
        )
        to_email = request.user.email

        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()

        data = {"order_number": order.order_number, "transID": payment.payment_id}
        return JsonResponse(data)
    else:
        # Handle the case when no matching order is found
        return HttpResponse("Order not found.")



def cash_on_delivery(request,number):
    url = request.META.get("HTTP_REFERER")
    orders = Order.objects.filter(
        user=request.user, is_ordered=False, order_number=number
    )
    if orders.exists():
        order = (
            orders.last()
        )  # You may want to add additional logic if there are multiple matching orders
        
        coupon_discount = 0 

        # Check if the order has a coupon applied
        if order.coupon:
            coupon_discount = order.coupon.discount_price
        payment = Payment(
            user=request.user,
            payment_id=number,
            payment_method="COD",
            amount_paid=order.order_total - coupon_discount,
            status="Completed",
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_item = ShopCart.objects.filter(user=request.user)
        for item in cart_item:
            orderproduct = OrderProduct()
            orderproduct.order = order
            orderproduct.payment = payment
            orderproduct.user = request.user
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            orderproduct.variant = item.variant
            orderproduct.price = item.variant.price
            orderproduct.grand_total = order.order_total - coupon_discount
            orderproduct.ordered = True
            orderproduct.save()

            variant = Variants.objects.get(id=item.variant.id)
            variant.quantity -= item.quantity
            variant.save()

        ShopCart.objects.filter(user=request.user).delete()
        mail_subject = "Thank you for your order"
        message = render_to_string(
            "order_recieved_email.html", {"user": request.user, "order": order}
        )
        to_email = request.user.email

        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()
        order_products = OrderProduct.objects.filter(order=order, user=request.user)
        context = {
                "order_products": order_products,
            }
        return render(request, "success.html",context)
    else:
        return HttpResponseRedirect(url)


@csrf_exempt
def wallet_payment(request, number):
    user_wallet = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user, is_ordered=False, order_number=number).last()

    if orders and user_wallet.wallet >= orders.order_total:
        coupon_discount = 0 

        # Check if the order has a coupon applied
        if orders.coupon:
            coupon_discount = orders.coupon.discount_price

        payment = Payment(
            user=request.user,
            payment_id=number,
            payment_method="Wallet",
            amount_paid=orders.order_total - coupon_discount,
            status="Completed",
        )
        payment.save()

        orders.payment = payment
        orders.is_ordered = True
        orders.save()

        cart_items = ShopCart.objects.filter(user=request.user)
        for item in cart_items:
            order_product = OrderProduct(
                order=orders,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                variant=item.variant,
                price=item.variant.price,
                grand_total = orders.order_total - coupon_discount,
                ordered=True,
            )
            order_product.save()

            variant = Variants.objects.get(id=item.variant.id)
            variant.quantity -= item.quantity
            variant.save()

        order_total_decimal = Decimal(str(orders.order_total))    
        user_wallet.wallet -= order_total_decimal
        user_wallet.save()

        wallet_history = Payementwallet(
            user=request.user,
            wallet=orders.order_total,
            paymenttype="Debit",
        )
        wallet_history.save()

        cart_items.delete()

        # Send order confirmation email
        mail_subject = "Thank you for your order"
        message = render_to_string(
            "order_recieved_email.html", {"user": request.user, "order": orders}
        )
        to_email = request.user.email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()

        order_products = OrderProduct.objects.filter(order=orders, user=request.user)
        context = {
            "order_products": order_products,
        }
        success_message = "your payment was success"
        return JsonResponse({"success": success_message, "message": success_message})

       
  
    else:
        error_message = "Your wallet balance is insufficient for this transaction."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"error": error_message, "message": error_message})
        else:
            messages.error(request, error_message)
            return render(request, "payment.html", {"order": orders})


def order_complete(request):
    order_number = request.GET.get("order_number")
    
    try:
        orders = Order.objects.filter(order_number=order_number, is_ordered=True)

        if orders.exists():
       
            order = orders.last()

            order_products = OrderProduct.objects.filter(order=order, user=request.user)
            context = {
                    "order_products": order_products,
                }
            return render(request, "success.html",context)
        else:
            # Handle the case where no orders match the criteria
            return HttpResponse("Order not found.")
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return HttpResponseRedirect("/")
    

def success(request):
    order_products = OrderProduct.objects.filter(user=request.user).last()
    context = {
            "order_products": order_products,
        }
    return render(request,'success.html',context)
    

