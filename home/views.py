from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from home.form import ContactForm
from user.models import WishlistItem
from order.models import CartView, Order, OrderProduct, ShopCart
from order.views import _cart_id
from product.models import Comment, ImageTypes, Images, Product, Category, Variants
from .models import ContactMessage, Setting
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.db.models import *
from django.db.models import Avg

# Create your views here.


# home page.........................................

@never_cache
def index(request):
    try:
        setting = Setting.objects.get(pk=1)
    except Setting.DoesNotExist:
        setting = None

    category = Category.objects.all()
    products_new_arrivals = Product.objects.filter(status=True).order_by("id")[:10]
    products_best_sellers = Product.objects.filter(status=True).order_by("?")[:10]

    # Check if user is authenticated
    wishlist_product_ids = []
    if request.user.is_authenticated:
        # Get the user's wishlist items
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        # Extract the product IDs from the wishlist items
        for item in wishlist_items:
            if item.product:
                wishlist_product_ids.append(item.product.id)
    context = {
        "setting": setting,
        "products_new_arrivals": products_new_arrivals,
        "products_best_sellers": products_best_sellers,
        "category": category,
        "wishlist_product_ids": wishlist_product_ids,
    }
    return render(request, "index.html", context)




# home page.........................................


# about-page.........................................
def aboutus(request):
    try:
        setting = Setting.objects.get(pk=1)
    except Setting.DoesNotExist:
        setting = None

    context = {
        "setting": setting,
    }
    return render(request, "about.html", context)


# about-page-end.........................................


# contact-page.........................................
def contact(request):
    try:
        setting = Setting.objects.get(pk=1)
    except Setting.DoesNotExist:
        setting = None
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data["name"]  # get form input data
            data.email = form.cleaned_data["email"]
            data.subject = form.cleaned_data["subject"]
            data.message = form.cleaned_data["message"]
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            messages.success(
                request, "Your message has ben sent. Thank you for your message."
            )
            return HttpResponseRedirect("/contact/")
    form = ContactForm

    context = {
        "setting": setting,
        "form": form,
    }
    return render(request, "contact.html", context)


# contact-page-end.........................................











# search-product..........................................
def search(request):
    products=Product.objects.filter(status=True).order_by('id')
    search=request.GET.get('query')
    categories_list = Category.objects.all()
    if search:
        products = products.filter(
            Q(title__icontains=search) |
            Q(category__title__icontains=search)  
        )
        context ={
        'products':products,
        'categories_list':categories_list 
        }    
        return render(request,'search_product.html',context)
    return render(request, "search_page.html")

def get_product(request):
    search = request.GET.get('search')  
    pro_list = []

    if search:
        obj = Product.objects.filter(title__icontains=search)

        for i in obj:
            pro_list.append({
                'title': i.title
            })

    return JsonResponse({
        'status': True,
        'pro_list': pro_list
    })

# search-product-end..........................................


# product-detail...............................................
def product_detail(request, id):
    unique_size_ids = []  # Initialize a list to keep track of unique size IDs
    unique_sizes = []
    query = request.GET.get("q")
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)

    comments = Comment.objects.filter(product_id=id)
    comment_rate = Comment.objects.filter(rate=id)

    in_cart = ShopCart.objects.filter(
        cart_item__cart_id=_cart_id(request), product=product
    ).exists()
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product=product
            ).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    product_category = product.category
    context = {
        "category": category,
        "product": product,
        "in_cart": in_cart,
        "images": images,
        "comments": comments,
        "comment_rate": comment_rate,
        "orderproduct": orderproduct,
        'product_category':product_category
    }

    if product.variant != "None":  # Product have variants
        if request.method == "POST":  # if we select color
            variant_id = request.POST.get("variantid")
            variant = Variants.objects.get(
                id=variant_id
            )  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw(
                "SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY id,size_id",
                [id],
            )
            query += (
                variant.title
                + " Size:"
                + str(variant.size)
                + " Color:"
                + str(variant.color)
            )
        else:
            variants = Variants.objects.filter(product_id=id).order_by("id")
            colors = Variants.objects.filter(
                product_id=id, size_id=variants[0].size_id
            ).order_by("id")
            sizes = Variants.objects.raw(
                "SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY id,size_id",
                [id],
            )
            variant = Variants.objects.get(id=variants[0].id)

        for rs in sizes:
            if rs.size_id not in unique_size_ids:
                unique_size_ids.append(rs.size_id)
                unique_sizes.append(rs)

        image_types = variant.get_image_types()
        context.update(
            {
                "unique_sizes": unique_sizes,
                "colors": colors,
                "variant": variant,
                "query": query,
                "image_types": image_types,
            }
        )
    return render(request, "product_detail.html", context)


# product-detail-end...............................................


def ajaxcolor(request):
    data = {}
    if request.POST.get("action") == "post":
        size_id = request.POST.get("size")
        productid = request.POST.get("productid")
        colors = Variants.objects.filter(
            product_id=productid, size_id=size_id
        ).order_by("id")
        context = {
            "size_id": size_id,
            "productid": productid,
            "colors": colors,
        }
        data = {"rendered_table": render_to_string("color_list.html", context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
