"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('register/', views.register, name='register_view'),
    re_path('^$|^login/$', views.login,name='login_view'),
    path('logout/', views.logout, name='logout_view'),
    path('main/', views.main,name='main_view'),
    path('list/', views.GoodsListView.as_view(),name='list_view'),
    path('detail/',views.show_goods_detail,name='detail_view'),
    path('add/', views.add_cart),
    path('show_cart/', views.show_cart,name='cart_view'),
    path('submit_orders/', views.submit_orders)

]
