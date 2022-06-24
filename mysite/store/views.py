from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView,DetailView
# Create your views here.

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