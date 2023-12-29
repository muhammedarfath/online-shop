"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from home import views
from order import views as OrderViews
from adminpanal import views as AdminViews


urlpatterns = [
    # user-urls.........................................
    path("", include("home.urls")),
    path("home/", include("home.urls")),
    path("product/", include("product.urls")),
    path("category_products/", include("shop.urls")),
    path("order/", include("order.urls")),
    path("user/", include("user.urls")),
    path("aboutus/", views.aboutus, name="about_us"),
    path("contact/", views.contact, name="contact"),
    path("search/", views.search, name="search"),
    path("get_product/",views.get_product,name="get_product"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("ajaxcolor/", views.ajaxcolor, name="ajaxcolor"),
    path("update_quantity/", OrderViews.update_quantity, name="update_quantity"),

    # user-urls-end.........................................
    
    
    # admin-urls.........................................
    path("admin/", admin.site.urls),
    path("adminpanel/", include("adminpanal.urls")),
    path("dashboard/", AdminViews.dashboard, name="dashboard"),
    path("admin_login/", AdminViews.admin_login, name="admin_login"),
    path("admin_logout/", AdminViews.admin_logout, name="admin_logout"),
    path("userdetails/", AdminViews.user_details, name="user_details"),
    
    path(
        "profile_details/<int:id>", AdminViews.profile_details, name="profile_details"
    ),
    path("user_unblock/<int:id>", AdminViews.user_unblock, name="user_unblock"),
    path("user_block/<int:id>", AdminViews.user_block, name="user_block"),
    path("productlist/", AdminViews.product_list, name="product_list"),
    path("addproduct/", AdminViews.add_product, name="add_product"),
    path("add_variant/<int:id>", AdminViews.add_variant, name="add_variant"),
    path("edit_product/<int:id>", AdminViews.edit_product, name="edit_product"),
    path("remove_variant/<int:id>", AdminViews.remove_variant, name="remove_variant"),
    path("order_list/", AdminViews.order_list, name="order_list"),
    path("cancel_list/", AdminViews.cancel_list, name="cancel_list"),
    path("return_list/", AdminViews.return_list, name="return_list"),
    path("refund/<int:id>", AdminViews.refund, name="refund"),
    path("order_details/<int:id>/", AdminViews.order_details, name="order_details"),
    path(
        "soft_delete_product/<int:id>/",
        AdminViews.soft_delete_product,
        name="soft_delete_product",
    ),
    path(
        "undelete_product/<int:id>/",
        AdminViews.undelete_product,
        name="undelete_product",
    ),
   
    path("admincoupon/",AdminViews.AdminCoupon.as_view(),name="admincoupon"),
    path("edit_coupon/<int:id>/",AdminViews.EditCoupon.as_view(),name="edit_coupon"),
    path("add_coupon/",AdminViews.AddCoupon.as_view(),name="add_coupon"),
    path("soft_delete_coupon/<int:id>/",AdminViews.soft_delete_coupon,name="soft_delete_coupon"),
    path("undelete_coupon/<int:id>/",AdminViews.undelete_coupon,name="undelete_coupon"),
    path("admincomments/",AdminViews.AdminComments.as_view(),name="admincomments"),
    path("comment_read/<int:id>/",AdminViews.CommentRead.as_view(),name="comment_read"),
    path("sales_report/",AdminViews.SalesReport.as_view(),name="sales_report"),
    path('generate_report/', AdminViews.generate_report, name='generate_report'),
    path('sales_report_pdf/', AdminViews.sales_report_pdf, name='sales_report_pdf'),


    
    # admin-urls-end.........................................
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
