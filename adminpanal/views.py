from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from coupons.models import Coupon
from order.models import Order, OrderProduct, Payment
from product.models import Brand, Category, Color, Comment, ImageTypes, Images, Product, Size, Variants
from user.models import Payementwallet, UserProfile
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.utils.text import slugify
from django.views import View
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import Count, Sum
from django.db.models import F, IntegerField
from django.db.models.functions import Cast
# Create your views here.



@never_cache
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.filter(is_superuser=True)
        product_counts = Product.objects.count()
        user_counts = User.objects.count()
        sales_count = Order.objects.filter(status=5).count()

        # Map status names to their corresponding integer values
        STATUS_MAPPING = {
            "New": 1,
            "Accepted": 2,
            "Preparing": 3,
            "OnShipping": 4,
            "Completed": 5,
            "Canceled": 6,  
            "Return": 7,     
        }

        # Use the mapped integer values in the specific_statuses list
        specific_statuses = ["Completed", "Return", "Canceled"]
        status_values = [STATUS_MAPPING[status] for status in specific_statuses]

        payment_counts = (
            Payment.objects.values("payment_method")
            .annotate(count=Count("payment_method"))
            .order_by("-count")
        )
 
        # Extract labels and data for chart.js
        labels = [entry["payment_method"] for entry in payment_counts]
        data = [entry["count"] for entry in payment_counts]
        
        status_counts = (
            Order.objects.filter(status__in=status_values)
            .values("status")
            .annotate(count=Count("status"))
            .order_by("-count")
        )
        # Extract labels and data for product status chart.js
        status_labels = [entry["status"] for entry in status_counts]
        status_data = [entry["count"] for entry in status_counts]

        # Query to get the number of orders per day in a month
        orders_per_day = (
            Order.objects.filter(create_at__month=12, create_at__year=2023)
            .values("create_at__day")
            .annotate(total_amount=Sum("order_total"))
            .order_by("create_at__day")
        )

      
        line_labels = [entry["create_at__day"] for entry in orders_per_day]
        line_data = [
            entry["total_amount"] for entry in orders_per_day
        ]  

        context = {
            "labels": labels,
            "data": data,
            "status_labels": status_labels,
            "status_data": status_data,
            "line_labels": line_labels,
            "line_data": line_data,
            "users": users,
            "product_counts":product_counts,
            "user_counts":user_counts,
            "sales_count":sales_count
            
        }
        return render(request, 'dashboard.html', context)
    else:
        return HttpResponseRedirect('/admin_login/')
    
    
    
    
@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return HttpResponseRedirect('/dashboard/')
    
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        if username.strip()=='' or password.strip()=='':
            messages.error(request,'fields cannot be empty')
        else:
            user=authenticate(username=username,password=password)
            
            if user and user.is_superuser:
                login(request,user)
                # request.session['admin_name']=username
                # print(username)
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.error(request ,'Invalid username or password')
                return HttpResponseRedirect('/admin_login/')

    return render(request,'admin_login.html')

def admin_logout(request):
    if request.user.is_authenticated and request.user.is_superuser:
        logout(request)
    return HttpResponseRedirect('/admin_login/')







def user_details(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.filter(is_superuser=False)  
        user_profiles = UserProfile.objects.filter(user__in=users) 
        
        context = {
            'users': users,
            'user_profiles': user_profiles,
        }
        return render(request, 'user_details.html', context)



def profile_details(request,id):
    user = get_object_or_404(User,id=id)
    profile = get_object_or_404(UserProfile,user=user) 

    context={
        'profile':profile,
        'user':user
    }
    return render(request,'user_full_details.html',context)






def user_unblock(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        user=get_object_or_404(User,id=id)
        user.is_active= True
        user.save()
        # print('dd')
        messages.success(request ,'This user is UnBlocked')
        return HttpResponseRedirect('/userdetails/')
    else:
        return HttpResponseRedirect('/admin_login/')
    
def user_block(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = get_object_or_404(User, id=id)
        user.is_active = False
        user.save()
        # print('ddddddddd')
        
        messages.success(request ,'This user is Blocked')
        return HttpResponseRedirect('/userdetails/')
    else:
        return HttpResponseRedirect('/admin_login/')    
    
    
    
def product_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        product=Product.objects.all()
        categories = Category.objects.all()
        brand = Brand.objects.all()
        context={
            'product':product,
            'categories':categories,
            'status_choices': Product.STATUS,
            'variant_choices': Product.VARIANTS,
            'brand':brand,
        }
        return render(request,'product_list.html',context)   
    else:
        return HttpResponseRedirect('/admin_login/')  
    
    
    

def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST['name']
            keyword = request.POST['keyword']
            description = request.POST['description']
            category_name = request.POST.get('category')
            brand_name = request.POST.get('brand')
            details = request.POST['details']
            sale_price = request.POST['saleprice']
            price = request.POST['price']
            status = request.POST.get('status')
            variant = request.POST.get('variant')
            images = request.FILES.get('image')
            variant_images = request.FILES.getlist('images')
            
            # Field validation checks

            
            if not name or not keyword or not description or not category_name or not brand_name or not details or not sale_price or not price or not status or not variant or not images or not variant_images :
                messages.error(request, 'Please fill in all the required fields.')
                return redirect('product_list')

            
            
            # Category validation
            category, created = Category.objects.get_or_create(title=category_name)
            brand, created = Brand.objects.get_or_create(name=brand_name)
            
            existing_product_by_name = Product.objects.filter(
                title=name,
                category=category
            )

            existing_product_by_image = Product.objects.filter(
                image=images
            )

            if existing_product_by_name.exists() or existing_product_by_image.exists():
                existing_name = existing_product_by_name.first().title if existing_product_by_name.exists() else ''
                existing_image = existing_product_by_image.first().image.url if existing_product_by_image.exists() else ''
                error_message = f"A similar product already exists. Please change name: '{existing_name}' or image: '{existing_image}'"
                messages.error(request, error_message)
                return redirect('product_list')



            # Generate a unique slug based on the title
            slug = slugify(name[:50])

            i = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{slug}-{i}"
                i += 1

            product = Product.objects.create(
                title=name,
                keywords=keyword,
                description=description,
                category=category,
                brand=brand,
                detail=details,
                price=price,
                minamount=sale_price,
                image=images,
                slug=slug,
                status=status,
                variant=variant,
            )
            product.save()
            product_id=Product.objects.filter(id=product.id)
            
            for img in variant_images:
                photo = Images.objects.create(product=product, image=img)
                photo.save()

            messages.error(request, 'Please add in product variants.')
            return redirect('add_variant', id=product.id)


        return render(request, 'product_list.html')
    else:
        return HttpResponseRedirect('/admin_login')

def add_variant(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    photo=Images.objects.filter(product=id)
    color=Color.objects.all()
    size=Size.objects.all()
    imagelist = ImageTypes.objects.annotate(image_id_int=Cast('image_id', IntegerField())).order_by('-image_id_int')

    context={
        'photo':photo,
        'color':color,
        'size':size,
        'imagelist':imagelist
    }
    if  request.method == 'POST':
        imageid=request.POST['imageid']
        imagetypes = request.FILES.getlist('imagetypes') 
        if imagetypes:
            for img_type in imagetypes:
                image_type_obj=ImageTypes.objects.create(image_id=imageid, image=img_type)
                image_type_obj.save()       
            messages.success(request,'Image variants save')
            return HttpResponseRedirect(url)
        name=request.POST['name']
        color_id=request.POST['color']
        price=request.POST['price']
        size_id=request.POST['size']
        image=request.POST['image']
        quantity=request.POST['quantity']
        variantypes = [i.image_id for i in ImageTypes.objects.all()]
        image_ids = []
        for x in variantypes:
            selected_values = request.POST.getlist('selectedImages[]')
            image_ids = [int(value) for value in selected_values]   
            context.update({
                'image_ids':image_ids
            }) 
        required_fields = [name, color_id, price, size_id, image, quantity]
        if not all(required_fields):
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('add_variant', id=product.id)
        color_instance = get_object_or_404(Color, name=color_id)
        size_instance = get_object_or_404(Size, name=size_id)
        existing_variant = Variants.objects.filter(product=product, color=color_instance, size=size_instance, image_id=image)

        if existing_variant.exists():
            messages.error(request, 'This variant already exists for the product.')
            return redirect('add_variant', id=product.id)
                
        color= Color.objects.get(name=color_id)
        size= Size.objects.get(name=size_id)

        variant = Variants.objects.create(title=name, product=product, color=color, size=size, image_id=image, quantity=quantity, price=price)
        for x in image_ids:
            image_objects = ImageTypes.objects.filter(image_id=x)
            for image_obj in image_objects:
                variant.image_types.add(image_obj)


        messages.success(request, 'Variant Added')
        return HttpResponseRedirect(url)
    return render(request,'add_variant.html',context) 




def edit_product(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = get_object_or_404(Product, id=id)
        variants = Variants.objects.filter(product=product)
        categories = Category.objects.all()
        brand = Brand.objects.all()
        images = Images.objects.filter(product=id)
        # variant = Variants.objects.filter(product=id)
        color = Color.objects.all()
        size = Size.objects.all()
        
        if request.method == 'POST':
            #product fields
            title = request.POST['name']
            description = request.POST['description']
            detail = request.POST['details']
            price = request.POST['price1']
            amount = request.POST['price2']
            status = request.POST['status']
            variant = request.POST['variant']
            image = request.FILES.get('image')
            category_id = request.POST['category']
            brand_id = request.POST['brand']
            category = get_object_or_404(Category, id=category_id)
            brand = get_object_or_404(Brand, id=brand_id)
            
            # variant fields 
            for var in variants:
                # Assuming you have a unique identifier for each variant, like variant_id
                variant_id = var.id

                # Retrieve form data for the current variant
                vtitle = request.POST[f'vtitle_{variant_id}']
                color_id = request.POST[f'color_{variant_id}']
                size_id = request.POST[f'size_{variant_id}']
                image_id = request.POST[f'image_id_{variant_id}']
                quantity = request.POST[f'quantity_{variant_id}']
                vprice = request.POST[f'vprice_{variant_id}']

                # Get the color and size objects based on their IDs
                color = get_object_or_404(Color, id=color_id)
                size = get_object_or_404(Size, id=size_id)

                # Update the variant with the new values
                var.title = vtitle.strip()
                var.color = color
                var.size = size
                var.image_id = image_id
                var.quantity = quantity
                var.price = vprice
                var.save()
                        
 

            if not title or not description or not detail or not status or not variant or not category or \
            (float(price) < 0 if price else True) or (float(amount) < 0 if amount else True):
                return HttpResponse("Please fill in all the required fields and provide valid numerical values for price and amount.")
            
            
            
   
            # If all validations pass, continue with the update logic
            product.title = title
            product.description = description
            product.detail = detail
            product.price = price
            product.amount = amount
            product.status = status
            product.variant = variant
            if image:
                product.image = image
            product.category = category
            product.brand = brand

            
            variant_image = request.FILES.getlist('variant_images')
            if variant_image:
                images.delete()
                for image in variant_image:
                    images = Images(product=product, image=image)
                    images.save()
            product.save()    
            
            

 
            messages.success(request, 'Edit Successfully')
            return HttpResponseRedirect('/productlist/')   
            


        context = {
            'categories': categories,
            'product': product,
            'variants':variants,
            'images': images,
            'product_status': Product.STATUS,
            'product_variant': Product.VARIANTS,
            'color':color,
            'size':size,
            'brand':brand,
            
        }

        return render(request, 'edit_product.html', context)
    else:
        return HttpResponseRedirect('/admin_login/')
  
  
  
  
def remove_variant(request, id):
    url = request.META.get('HTTP_REFERER')
    try:
        variant = Variants.objects.get(id=id)
        variant.delete()
    except Variants.DoesNotExist:
        return render(request, '404.html')
    
    return HttpResponseRedirect(url)
  
  
def soft_delete_product(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = get_object_or_404(Product, pk=id)
        product.status = False
        product.save()
        return HttpResponseRedirect('/productlist/') 
    else:
        return HttpResponseRedirect('/admin_login/')



def undelete_product(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = get_object_or_404(Product, pk=id)
        product.status = True 
        product.save()
        return HttpResponseRedirect('/productlist/') 
    else:
        return HttpResponseRedirect('/admin_login/')   
    
    



def order_list(request):
    orders = OrderProduct.objects.all().order_by('-create_at')
    context = {
        'orders': orders,
        'order_status': Order.ORDERSTATUS,
    }

    if request.method == 'POST':
        selected_status = request.POST['orderStatus']
        selected_order_id = request.POST['orderId']
        selected_product = request.POST['variantId']
        orders = OrderProduct.objects.get(order=selected_order_id)
        user_wallet = UserProfile.objects.get(user=orders.order.user)

        try:
            selected_order = OrderProduct.objects.get(order=selected_order_id, variant=selected_product)
        except OrderProduct.DoesNotExist:
            print(f"Order with order_id={selected_order_id} and variant_id={selected_product} does not exist.")
            # Log or handle the exception appropriately
            return HttpResponseRedirect('/order_list/')

        if selected_order.variant.id == int(selected_product):
            selected_order.order.status = selected_status
            selected_order.order.save()

            if selected_status == '5':
                selected_order.status = "Accepted"
                selected_order.save()
            elif selected_status == '6':
                if orders.order.coupon:
           
                    total = orders.order.order_total - orders.order.coupon.discount_price
                    user_wallet.wallet += Decimal(str(total))
                else:
                    user_wallet.wallet += Decimal(str(orders.order.order_total))
                
                wallet_details = Payementwallet(user=orders.order.user)
                wallet_details.paymenttype = "Credit"
                wallet_details.wallet = Decimal(str(orders.order.order_total))
                mail_subject = "Your order admin has been cancelled your refund successfully approved."
                message = render_to_string(
                        "refund_recieved_email.html", {"user": orders.order.user, "wallet": orders.order.order_total}
                    )
                to_email = orders.order.user.email
                send_mail = EmailMessage(mail_subject, message, to=[to_email])
                send_mail.send()
                
                user_wallet.save()
                wallet_details.save()
                orders.save()
                orders.order.save()
            else:
                pass    
                    
                
            
                    

        return HttpResponseRedirect('/order_list/')

    return render(request, 'orders_list.html', context)

def cancel_list(request):
        
    orders = OrderProduct.objects.all().order_by('-create_at')
    context={
        'orders':orders,
        'order_status':Order.ORDERSTATUS,

    }

    return render(request,'cancel_order.html',context)

def return_list(request):
    orders = OrderProduct.objects.all().order_by('-create_at')
    context={
        'orders':orders,
        'order_status':Order.ORDERSTATUS,

    }

    return render(request,'return_order.html',context)
    

def order_details(request,id):
    order_details = Order.objects.get(id=id)
    full_name = f"{order_details.first_name} {order_details.last_name}"
    order_product = OrderProduct.objects.filter(order=order_details).last()
    tax = (2 * order_product.price) / 100
    grand_total = order_product.quantity * (order_product.price + tax)


    

    context={
        'order_details':order_details,
        'order_status':Order.ORDERSTATUS,
        'full_name':full_name,
        'order_product':order_product,
        'grand_total':grand_total
    }
    return render(request,'order_details.html',context)

def refund(request, id):
    url = request.META.get('HTTP_REFERER')
    order_product = OrderProduct.objects.get(id=id)
    user_wallet = UserProfile.objects.get(user=order_product.order.user)
    if order_product.status == 'Canceled':
        order_product.order.status = 6
    else:
        order_product.order.status = 7 
        
    if order_product.order.coupon:
        total = order_product.order.order_total - order_product.order.coupon.discount_price
        user_wallet.wallet += Decimal(str(total))
    else:
        user_wallet.wallet += Decimal(str(order_product.order.order_total))
    
    wallet_details = Payementwallet(user=order_product.order.user)
    wallet_details.paymenttype = "Credit"
    wallet_details.wallet = Decimal(str(order_product.order.order_total))
    mail_subject = "Your refund has been successfully approved."
    message = render_to_string(
            "refund_recieved_email.html", {"user": order_product.order.user, "wallet": order_product.order.order_total}
        )
    to_email = order_product.order.user.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.send()
    
    wallet_details.save()
    user_wallet.save()
    order_product.order.save()
    return HttpResponseRedirect(url)
  
    





class AdminCoupon(View):
    template_name = "admincoupon.html"

    def get(self, request):
        coupons = Coupon.objects.all()
        context = {
            "coupons": coupons
        }
        return render(request, self.template_name, context)
    
    
class EditCoupon(View):
    template_name = "edit_coupon.html"
    def get(self,request,id):
        coupon = Coupon.objects.get(id=id)
        context = {
            "coupon" :coupon
        }    
        return render(request,self.template_name,context)
        
    def post(self, request, id):
            if request.method == "POST":
                coupon = Coupon.objects.get(id=id)

                # Retrieve form data
                coupon_name = request.POST.get('name')
                coupon_code = request.POST.get('code')
                status = request.POST.get('status')
                discount = request.POST.get('discount_price')
                minimum_amount = request.POST.get('minimum_amount')
                coupon_expiration_time = request.POST.get('coupon_expiration_time')
                image = request.FILES.get('image')

                # Update Coupon instance
                coupon.offer_name = coupon_name
                coupon.code = coupon_code
                coupon.is_expired = status == 'true'
                coupon.discount_price = discount
                coupon.minimum_amount = minimum_amount
                
                # Handle expiration time format conversion
                if coupon_expiration_time:
                    coupon.expiration_time = coupon_expiration_time

                if image:
                    coupon.image = image
                coupon.save()
                messages.success(request,'coupon edit successfully')

                return HttpResponseRedirect('/admincoupon/')

    
class AddCoupon(View):
    def post(self, request):
        # Retrieve data from the form
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        coupon_image = request.FILES.get('coupon_image')  # Handle file upload
        coupon_discount = request.POST.get('coupon_discount')
        coupon_minimum_amount = request.POST.get('coupon_minimum_amount')
        coupon_expiration_time = request.POST.get('coupon_expiration_time')
        

        # Create and save the Coupon object
        coupon = Coupon(
            user=request.user,  # Assuming you have a logged-in user
            offer_name=coupon_name,
            code=coupon_code,
            image=coupon_image,
            discount_price=coupon_discount,
            minimum_amount=coupon_minimum_amount,
            expiration_time=coupon_expiration_time,
        )
        coupon.save()
        return HttpResponseRedirect('/admin_login/')  
    
    
    
    
    
    
def soft_delete_coupon(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        coupon = get_object_or_404(Coupon, pk=id)
        coupon.active = False
        coupon.save()
        return HttpResponseRedirect('/admincoupon/') 
    else:
        return HttpResponseRedirect('/admin_login/')



def undelete_coupon(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        coupon = get_object_or_404(Coupon, pk=id)
        coupon.active = True 
        coupon.save()
        return HttpResponseRedirect('/admincoupon/') 
    else:
        return HttpResponseRedirect('/admin_login/')      
    
    
class AdminComments(View):
    template_name="comments.html"
    def get(self,request):
        comment=Comment.objects.all().order_by('-id')
        context={
            'comment':comment
        }
        return render(request,self.template_name,context)     
    
class CommentRead(View):
    def get(self,request,id):
        comment = get_object_or_404(Comment, id=id)
        comment.status = False
        comment.save()
        return HttpResponseRedirect('/admincomments/')
        
class SalesReport(View):
    template_name = "sales_report.html"

    def get(self, request):
        order_instance = Order()
        
        context={
            'order_status_choices':order_instance.ORDERSTATUS
        }
        return render(request, self.template_name,context)
    

def generate_report(request):
    try:
        order_instance = Order()
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        status = request.GET.get("status")

        request.session["start_date"] = start_date
        request.session["end_date"] = end_date
        request.session["status"] = status

        filtered_orders = Order.objects.filter(
            create_at__range=[start_date, end_date],
            status=status if status else None,
        ).order_by("create_at")

        context = {
            "sales": filtered_orders,
            'order_status_choices':order_instance.ORDERSTATUS
        }

        return render(request, "sales_report.html", context)
    except Exception as e:
        print(e)
        return render(request, "404.html")


def sales_report_pdf(request):
    try:
        start_date = request.session["start_date"]
        end_date = request.session["end_date"]
        status = request.session["status"]
        


        filtered_orders = Order.objects.filter(
            create_at__range=[start_date, end_date],
            status=status if status else None,
        ).order_by("create_at")

        data = [
            [
                "ID",
                "User",
                "Order Number",
                "Order Date",
                "Status",
                "Tax",
                "Shipping",
                "Grand Total",
            ]
        ]
        
        for sale in filtered_orders:
            data.append(
                [
                    sale.id,
                    sale.user.username,
                    sale.order_number,
                    sale.create_at,
                    sale.get_status_display(),
                    sale.tax,
                    40,
                    sale.order_total,
                ]
            )

        # Create PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        table = Table(data)

        # Apply table styles
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )

        table.setStyle(style)
        doc.build([table])

        request.session.pop("start_date", None)
        request.session.pop("end_date", None)
        request.session.pop("status", None)

        return response
    except Exception as e:
        print(e)
        return render(request, "404.html")

