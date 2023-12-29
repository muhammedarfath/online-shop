from django.urls import path
from . import views

app_name="user"

urlpatterns = [
    path("", views.index, name="user_index"),
    path("update/", views.user_update, name="user_update"),
    path("password/", views.user_password, name="user_password"),
    path("orders/", views.UserOrders.as_view(), name="orders"),
    path("favorites/",views.WishlistPage.as_view(),name="favorites"),
    path("signup/",views.signup_form, name="signup"),
    path("login/", views.login_form, name="login"),
    path("logout/", views.logout_func, name="logout"),
    path("otp/", views.otp_func, name="otp"),
    path('newotp/',views.newotp, name='newotp'),
    path('wallet/',views.Wallet.as_view(),name="wallet"),
    path("user_order_details/<int:id>/", views.UserOrderDetails.as_view(), name="user_order_details"),
    path("comments/", views.user_comments, name="user_comments"),
    path("coupon/",views.CouponPage.as_view(),name="coupon"),
    path("remove_wishlist/<int:id>/",views.RemoveWishlist.as_view(),name="remove_wishlist"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path("resetpassword_validate/<uidb64>/<token>/",views.resetpassword_validate,name="resetpassword_validate",),
    path("resetpassword/", views.resetpassword, name="resetpassword"),
    path("userprofile/", views.userprofile, name="userprofile"),
    path("<str:room_name>/", views.room, name="room"),
    path("order_return/<int:id>/",views.OrderReturn.as_view(),name="order_return"),
    path("cancel_order/<int:id>/", views.CancelOrder.as_view(), name="cancel_order"),
    path("add_to_wishlist/<int:id>/",views.AddToWishlist.as_view(),name="add_to_wishlist"),
    path('delete_comment/<int:id>/',views.DeleteComment.as_view(),name="delete_comment"),
    path('invoice/<int:id>/',views.Invoice.as_view(),name="Invoice"),
    
    
    
    
 
]
