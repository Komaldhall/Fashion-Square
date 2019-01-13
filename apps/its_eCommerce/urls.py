from django.urls import path
from . import views 

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    path('ship', views.ship),
    path('buy', views.buy),
    path('remove', views.remove),
    path('quantity', views.quantity),
    path('', views.index),
    path('men', views.showmen),
    path('women', views.showwomen),
    path('kid', views.showkid),
    path('boy', views.showkid),
    path('girl', views.showkid),
    path('register', views.register),
    path('showProduct', views.showProd),
    path('add', views.add),
    path('cart', views.cart),
    path('order', views.order),
    path('success', views.success),
    path('search', views.search),
    
]