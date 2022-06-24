from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView,DetailView
# Create your views here.
import random
import datetime
#register
from store.forms import RegistrationForm, LoginForm
from .models import Customer,Goods,Orders,OrderLineItem

#login
def login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            c = Customer.objects.get(id=userid)

            if c is not None and c.password == password:
                # put id into http session
                request.session['customer_id'] = c.id
                return HttpResponseRedirect('/main/')
    else:
        form = LoginForm()

    return render(request,"login.html",{"form":form})
#register
def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            new_customer = Customer()
            new_customer.id = form.cleaned_data["userid"]
            new_customer.name = form.cleaned_data["name"]
            new_customer.password = form.cleaned_data["password1"]
            new_customer.birthday = form.cleaned_data["birthday"]
            new_customer.phone = form.cleaned_data["phone"]

            new_customer.save()

            return render(request,'customer_reg_success.html')
    else:
        form = RegistrationForm()

    return render(request,"customer_reg.html",{"form":form})

def main(request):# check session
    if not request.session.has_key('customer_id'):
        print("please login")
        return HttpResponseRedirect("/login/")
    return render(request,'main.html')

class GoodsListView(ListView):
    model = Goods
    ordering = ['id']
    # template
    template_name = 'goods_list.html'

def show_goods_detail(request):
    goodsid = request.GET['id']
    goods = Goods.objects.get(id=goodsid)

    return render(request,'goods_detail.html',{'goods':goods})

def add_cart(request):
    if not request.session.has_key('customer_id'):
        print("need login")
        return HttpResponseRedirect("/login/")

    goodsid = int(request.GET['id'])
    goodsname = request.GET['name']
    goodsprice = float(request.GET['price'])

    # judge whether there is a cart data
    if not request.session.has_key('cart'):
        #empty
        request.session['cart'] = []

    cart = request.session['cart']
    flag = 0
    for item in cart:
        #[id,price...]
        if item[0] == goodsid:
            item[3] +=1
            flag = 1
            break
    if flag == 0:# new item
        item = [goodsid,goodsname,goodsprice,1]
        cart.append(item)
    request.session['cart'] = cart

    print(cart)

    page = request.GET['page']
    if page == 'list':
        return HttpResponseRedirect('/list/')
    else:
        return HttpResponseRedirect('/detail/?id='+str(goodsid))

def show_cart(request):
    if not request.session.has_key('customer_id'):
        print('not login')

        return HttpResponseRedirect("/login")

    if not request.session.has_key('cart'):
        print('empty cart')

        return render(request,'cart.html',{'list':[],'total':0.0})

    cart = request.session['cart']
    list = []
    total = 0.0
    for item in cart:
        subtotal = item[2] * item[3]
        total += subtotal
        #build a new item for reference
        new_item = (item[0],item[1],item[2],item[3],subtotal)
        list.append(new_item)
    return render(request,'cart.html',{'list':list,'total':total})

def submit_orders(request):
    if request.method == 'POST':
        orders = Orders()
        #generate id, time slot + random
        n = random.randint(0,9)
        d = datetime.datetime.today()
        ordersid = str(int(d.timestamp()*1e6))+str(n)
        orders.id = ordersid
        orders.order_date = d
        orders.status = 1
        orders.total = 0.0
        orders.save()

        cart = request.session['cart']
        total = 0.0

        for item in cart:

            goodsid = item[0]
            goods = Goods.objects.get(id=goodsid)

            quantity = request.POST['quantity_' + str(goodsid)]

            try:
                quantity = int(quantity)
            except:
                quantity = 0

            #cal subtotal
            subtotal = item[2] * quantity
            total += subtotal

            order_line_item = OrderLineItem()
            order_line_item.quantity = quantity
            order_line_item.goods = goods
            order_line_item.orders = orders
            order_line_item.subtotal = subtotal

            order_line_item.save()

        orders.total = total
        orders.save()

        #del cart session
        del request.session['cart']

        return render(request,'order_finish.html',{'ordersid': ordersid})

def logout(request):
    if request.session.has_key('customer_id'):
        del request.session['customer_id']
        if request.session.has_key('cart'):
            del request.session['customer_id']

    return HttpResponseRedirect('/login/')
