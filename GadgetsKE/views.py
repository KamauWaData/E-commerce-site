from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from urllib import request
from django.views import View
from .models import products, Customer, Cart #, Payment, OrderPlaced
from django.shortcuts import render, redirect
from .forms import registrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings

# Create your views here.
def home(request):
    return render(request,"app/index.html")

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product = products.objects.filter(category=val)
        title = products.objects.filter(category=val).values('title')
        return render(request, "app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = products.objects.filter(title=val)
        title = products.objects.filter(category=product[0].category).values('title').annotate(total=Count(''))
        return render(request, "app/category.html",locals())

class productDetail(View):
    def get(self, request,pk):
        product = products.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
        def get(self, request):
            form = registrationForm()
            return render(request,"app/registration.html",locals())
        def post(self, request):
            form = registrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Yay! You have been Successfully Registered")
            else: 
                messages.warning(request, "Invalid Input Data")
            return render(request,"app/registration.html",locals()) 

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/peofile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()

            messages.success(request, 'Congarts! Profile Updated Successfully')
        else:
            messages.warning(request, "Invalid Data Input")
        return render(request, 'app/profile.html', locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddresss.html',locals())
    
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            ##user = request.user
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save

            messages.success(request, 'Congarts! Profile Updated Successfully')
        else:
            messages.warning(request, "Invalid Data Input")
        return redirect('address')
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = products.objects.get(id=product_id)
    Cart(user-user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount * value
        totalamount = amount + 150 
    return render(request, 'app/addtocart.html', locals())

class checkout(View):
    def get(self, request):
        user= request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        fAmount = 0
        for p in cart_items:
            value = p.quantity * p.product.discount
            fAmount = fAmount + value
            totalamount = fAmount + 150
            #mpesaAmount = int(totalamount * 100)
            #client = mpesa.Client(auth=(settings.MPESA_KEY_ID, settings.MPESA_KEY_SECRET))
            #data = ('amount': mpesaAmount, 'currency': 'KES', 'receipt':'oreder_rcptid_11)
            #payment_response = client.order.create(data=data)
            order_id = payment_response['id']
            order_status = payment_response['status']
            if order_status == 'created':
                payment = Payment(
                    user=user,
                    amount = totalamount,
                    mpesa_order_id = order_id,
                    mpesa_payment_status = order_status
                )
                payment.save()
        return render(request, 'app/checkout.html', locals())

#mpesa integration
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    #update payment status and payment id
    payment=Payment.objects.get(mpesa_order_id=order_id)
    payment.paid = True
    payment.mpesa_payment_id = payment_id
    payment()
    #save order details
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer, product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0

        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount * value
            totalamount = amount + 150 
        print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0

        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount * value
            totalamount = amount + 150 
        print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0

        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount * value
            totalamount = amount + 150 
        print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)