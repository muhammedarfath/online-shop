from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from product.models import Brand, Category, Filter_Price, Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from decimal import Decimal

# shop-page................................................................
def category_products(request):
    

    catid = request.GET.get('categories')
    braid = request.GET.get('brand')
    priceid = request.GET.get('filter_price')



    if catid:
        products = Product.objects.filter(category__id=catid, status=True).order_by("id")
        paginator = Paginator(products, 4)
        page = request.GET.get("page")
    elif braid:
        products = Product.objects.filter(brand__id=braid, status=True).order_by("id")
        paginator = Paginator(products, 4)
        page = request.GET.get("page") 
    elif priceid:
        products = Product.objects.filter(filter_price = priceid, status=True).order_by("id")   
        paginator = Paginator(products, 4)
        page = request.GET.get("page")      
    else:
        products = Product.objects.filter(status=True).order_by("id")
        paginator = Paginator(products, 4)
        page = request.GET.get("page")
    


    paged_product = paginator.get_page(page)
    categories_list = Category.objects.all()
    brand_list = Brand.objects.all()
    filter_price = Filter_Price.objects.all()
    
  
   


    context = {
        "products": paged_product,
        "categories_list": categories_list,
        "brand_list":brand_list,
        "active_category": int(catid) if catid else None,
        "active_brand": int(braid) if braid else None,
        'filter_price':filter_price


    }
    return render(request, "category_product.html", context)



# shop-page-end................................................................
