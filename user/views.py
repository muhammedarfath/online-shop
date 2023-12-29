from decimal import Decimal
import random
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from home.models import Setting
from coupons.models import Coupon
from order.models import CartView, Order, OrderProduct, ShopCart
from order.views import _cart_id
from product.models import Category, Comment, Product, Variants
from user.form import SignUpForm
from user.models import Payementwallet, UserProfile, WishlistItem
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

def index(request):
    return HttpResponse("user Page")


# User-login......................................................
@never_cache
def login_form(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                cart = CartView.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = ShopCart.objects.filter(cart_item=cart).exists()
                if is_cart_item_exists:
                    cart_item = ShopCart.objects.filter(cart_item=cart)
                    product_variant = []
                    for item in cart_item:
                        variant = item.variant
                        product_variant.append(variant)

                    cart_item = ShopCart.objects.filter(user=user)
                    ex_var_list = []
                    id = []

                    for item in cart_item:
                        existing_variant = item.variant
                        ex_var_list.append(existing_variant)
                        id.append(item.id)

                    for rs in product_variant:
                        if rs in ex_var_list:
                            index = ex_var_list.index(rs)
                            item_id = id[index]
                            item = ShopCart.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = ShopCart.objects.filter(cart_item=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass

            login(request, user)

            # Check if a UserProfile already exists for the user
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # If not, create a new UserProfile
                user_profile = UserProfile(user=user,image="images/user.jpeg")
                coupon = Coupon.objects.first()  # Get the first coupon, you may adjust this based on your logic
                user_profile.coupon = coupon
                user_profile.save()

            messages.success(request, "Login successfully")

            if not request.user.is_superuser:
                current_user = request.user
                userprofile = UserProfile.objects.get(user_id=current_user.id)
                request.session["userimage"] = userprofile.image.url
                url = request.META.get("HTTP_REFERER")
                try:
                    query = requests.utils.urlparse(url).query
                    # print(query,"hiiiiii")
                    params = dict(x.split("=") for x in query.split("&"))
                    if "next" in params:
                        nextpage = params["next"]
                        return HttpResponseRedirect(nextpage)

                except:
                    return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/")
        else:
            messages.error(
                request, "Login Error !! Username or Password is incorrect"
            )
            return HttpResponseRedirect("/user/login/")

    return render(request, "login_form.html")


# User-login-end......................................................


# User-logout......................................................
@never_cache
def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")


# User-logout-end......................................................


# forgot-password......................................................
def forgotpassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string(
                "rest_password_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            messages.success(
                request, "Password reset email has been sent to your email address"
            )
            return HttpResponseRedirect("/user/login/")
        else:
            messages.error(request, "Account does not exist")
            return HttpResponseRedirect("/user/forgotpassword/")

    return render(request, "forgot_password.html")


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "please reset your password")
        return HttpResponseRedirect("/user/resetpassword/")
    else:
        messages.success(request, "this link has been expired!")
        return HttpResponseRedirect("/user/login/")


def resetpassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session.get("uid")
            if uid is not None:
                user = User.objects.get(pk=uid)
                user.set_password(password)
                user.save() 
            messages.success(request, "Password Reset Successful")
            return HttpResponseRedirect("/user/login/")
        else:
            messages.error(request, "password do not match")
            return HttpResponseRedirect("/user/resetpassword/")
    return render(request, "resetpassword.html")


# forgot-password-end......................................................


# User-signup......................................................
def signup_form(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            
            otp = str(random.randint(1000, 9999))

            request.session['signup_username']=username
            request.session['signup_otp'] = otp
  



            subject = 'OTP Verification Code'
            message = f'Your OTP code for signup is: {otp}'
            from_email = 'coloshope@gmail.com'
            recipient_list = [email]
            
            # return HttpResponse(from_email)

            send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, 'Your account has been created!Please Enter OTP')
            return HttpResponseRedirect('/user/otp/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/user/signup/')

    return render(request, 'signup_form.html')


# User-signup-end......................................................


# Otp......................................................
def otp_func(request):
    if request.method == 'POST':
        otp_entered = request.POST['otp_entered']
        otp_saved = request.session.get('signup_otp')
        if otp_entered == otp_saved:
            # OTP is valid; remove it from the session
            del request.session['signup_otp']

            # Save the user
            username=request.session['signup_username']
            # print(username)
            user = User.objects.get(username=username)
            user.is_active = True
            user.is_otp=True
            user.save()
            messages.success(request, "Your registration is successful. You can now log in.")           
            return HttpResponseRedirect('/user/login/')  # Redirect to the login page or any other desired page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request,'otp.html')




def newotp(request):
    username=request.session.get('signup_username')
    user = User.objects.get(username=username)
    request.session.pop('signup_otp', None)
    if user.email:
        otp = str(random.randint(1000, 9999))
        request.session['signup_otp'] = otp
        subject = 'Resent OTP Verification Code'
        message = f'Your resent OTP code for signup is: {otp}'
        from_email = 'coloshope@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'resend OTP sent successfully. Please check your email.')
    else:
        messages.warning(request, 'Failed to resend OTP. Please try again.')

    return HttpResponseRedirect('/user/otp/')
# Otp-end......................................................


# User-profile......................................................
@login_required(login_url="/user/login/")  # Check login
def userprofile(request):
    current_user = request.user
    try:
        profile = UserProfile.objects.get(user=current_user)
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not added")
        return HttpResponseRedirect("/")

    if request.user.is_authenticated:
        cart_items = ShopCart.objects.filter(user=request.user)
    else:
        cart_user = CartView.objects.get(cart_id=_cart_id(request))
        cart_items = ShopCart.objects.filter(cart_item=cart_user)
    context = {
        "profile": profile,
        "current_user": current_user,
        "cart_items": cart_items,
    }
    return render(request, "user_profile.html", context)


@login_required(login_url="/user/login/")
def room(request, room_name):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    is_admin = user.is_staff  
    template_name = "adminchat.html" if is_admin else "chat.html"
    return render(request, template_name, {"room_name": room_name, "user_name": user.username,"profile":profile})




@login_required(login_url="/user/login/")  # Check login
def user_update(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        phone = request.POST["phone"]
        country = request.POST["country"]
        state = request.POST["state"]
        city = request.POST["city"]
        address = request.POST["address"]
        image = request.FILES.get("image")
        bannerimage = request.FILES.get("bannerimage")
        

        # Get or create the User instance based on the username
        user_form, created = User.objects.get_or_create(username=username)
        user_form.email = email
        user_form.first_name = firstname
        user_form.last_name = lastname
        user_form.save()

        # Get or create the UserProfile instance associated with the User
        profile, created = UserProfile.objects.get_or_create(user=user_form)
        profile.phone = phone
        profile.country = country
        profile.city = city
        profile.state = state
        profile.address = address
        if image:
            profile.image = image
        if bannerimage:
            profile.banner_image = bannerimage   
        profile.save()
        return HttpResponseRedirect("/user/userprofile/")
    else:
        # Retrieve the User and UserProfile instances for the currently logged-in user
        user_form = request.user  # Assuming the request.user is authenticated
        profile, created = UserProfile.objects.get_or_create(user=user_form)

    context = {
        "user_form": user_form,
        "profile": profile,
    }

    return render(request, "update_user.html", context)


@login_required(login_url="/user/login/")  # Check login
def user_password(request):
    
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return HttpResponseRedirect("/user/userprofile/")
        else:
            messages.error(
                request, "Please correct the error below.<br>" + str(form.errors)
            )
            return HttpResponseRedirect("/user/password/")
    else:
        profile = UserProfile.objects.get(user=request.user)
        form = PasswordChangeForm(request.user)
        context = {
            "profile": profile
        }
        return render(request, "user_password.html", {"form": form, **context})


    
@login_required(login_url="/user/login/")  # Check login
def user_comments(request):
    current_user = request.user
    profile = UserProfile.objects.get(user=request.user)
    comments = Comment.objects.filter(user_id=current_user.id)

    context = {
        "comments": comments,
        "profile":profile
    }
    return render(request, "user_comments.html", context)


class DeleteComment(View):
    def get(self,request,id):
        url = request.META.get("HTTP_REFERER")
        comment = Comment.objects.get(id=id)
        comment.delete()
        return HttpResponseRedirect(url)
        
        
    


class UserOrders(View):
    template_name = "user_order.html"

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
            "-create_at"
        )
        orderproducts = OrderProduct.objects.filter(order__in=orders, user=request.user).order_by("-id")

        context = {
            "orders": orders,
            "orderproducts": orderproducts,
            'profile':profile
        }
        return render(request, self.template_name, context)



class UserOrderDetails(View):
    template_name = "user_order_details.html"
    def get(self, request, id):
        orders = get_object_or_404(OrderProduct, id=id)
        colo = get_object_or_404(Setting)
        orderstatus = orders.order.status
        accepted_timestamp = orders.update_at if orders.update_at else orders.create_at
        seven_days_ago = accepted_timestamp + timezone.timedelta(days=7)
        time = timezone.now()
        context = {"orders": orders, "colo": colo, "orderstatus":orderstatus,"seven":seven_days_ago,"time":time}
        return render(request, self.template_name, context)


class CancelOrder(View):

    template_name = "user_order_details.html" 

    def post(self, request, id):
        if request.method == 'POST':
            reason = request.POST.get('cancel_reason')
            if not reason:
                messages.error(request,"Cancel reason is required.")
                return render(request, self.template_name)
                
            orders = get_object_or_404(OrderProduct, id=id)
            orders.user_note = reason
            orders.status = "Canceled"
            orders.save()
            return render(request, self.template_name)


class OrderReturn(View):
    
    def post(self, request, id):
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            reason = request.POST.get('return_reason')
            if not reason:
                messages.error(request,"return reason is required.")
                return HttpResponseRedirect(url)
            order_product = get_object_or_404(OrderProduct, id=id)
            # Check if the order was placed within the last 7 days since status became "Accepted"
            accepted_timestamp = order_product.update_at if order_product.update_at else order_product.create_at
            seven_days_ago = accepted_timestamp + timezone.timedelta(days=7)
            time = timezone.now()
            if time > seven_days_ago:
                messages.error(request, "You can only return the order within 7 days after it's accepted.")
                
                return HttpResponseRedirect(url)
            else:   
                orders = get_object_or_404(OrderProduct, id=id)
                orders.user_note = reason
                orders.status = "Return"
                orders.save()
                return HttpResponseRedirect(url)

    
   
class WishlistPage(View):
    
    template_name = "wishlist.html"
    
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/user/ligin/")
        profile = UserProfile.objects.get(user=request.user)
        wishitem = WishlistItem.objects.filter(user=request.user)
        
        context = {
            "wishitem": wishitem,
            "profile": profile
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        return render(request, self.template_name)
    
    
    
class AddToWishlist(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/user/login/")
        product = get_object_or_404(Product, id=id)
        variant = Variants.objects.filter(product=product).first()
        
        existing_wishlist_item = WishlistItem.objects.filter(user=request.user, variant=variant).first()
        cart_item = ShopCart.objects.filter(user=request.user, product=product)
        if not existing_wishlist_item:
            if not cart_item:
                WishlistItem.objects.create(user=request.user, variant=variant,product=product)
            else:
                messages.error(request,'this item is already added the cart')  
                return redirect('/order/shopcart/') 
                    
        else:
            messages.error(request,'this item is already added')  
            return redirect('/user/favorites/') 
        
        return redirect('/user/favorites/')
 
 
        
class RemoveWishlist(View):
    def get(self,request,id):
        product = WishlistItem.objects.get(id=id)  
        product.delete()
        return HttpResponseRedirect("/user/favorites/")
            
    
class CouponPage(View):
     template_name = "coupon.html"
     
     def get(self,request):
        coupon = Coupon.objects.filter(active=True) 
        profile = UserProfile.objects.get(user=request.user)
        context={
            'profile':profile,
            'coupon':coupon
        }
        return render(request,self.template_name,context)   
    
    
    
class Invoice(View):
    template_name = "order_complete.html"    
    def get(self,request,id):
        company = Setting.objects.get()
        order_products = get_object_or_404(OrderProduct ,id=id,user=request.user)
        subtotal = 0
        qty = 0
        tax=0

        qty += order_products.quantity
        subtotal += order_products.variant.price * order_products.quantity
            
        coupon_code = order_products.order.coupon.code if order_products.order.coupon else None
        coupon_discount = order_products.order.coupon.discount_price if order_products.order.coupon else 0   
        shipping = 40
        tax = (2 * subtotal) / 100
        grand_total = subtotal + tax - coupon_discount
        context = {
                "order_products": order_products,
                "subtotal": subtotal,
                "company": company,
                "qty": qty,
                "tax": tax,
                "shipping": shipping,
                "coupon_code": coupon_code,
                "coupon_discount": coupon_discount,
                "grand_total": grand_total,
            }
        return render(request,self.template_name,context)


class Wallet(View):
    template_name = "wallet.html"
    def get(self,request):
        
        try:
            user=request.user
            if user:
                profile = UserProfile.objects.get(user=user)
                wallet_history=Payementwallet.objects.filter(user=user).order_by('-created')
                return render(request,self.template_name,{'wallet_history': wallet_history,'profile':profile})
            else:
                messages.error(request,"Please login first")
                return HttpResponseRedirect("/user/login/")
        except Exception as e:
            print(e)
            return render(request,self.template_name,{'wallet_history': wallet_history,'profile':profile})

# User-profile-end......................................................
