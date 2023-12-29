
from . import views
from django.urls import path

urlpatterns = [
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('',views.index,name='index'),
]
