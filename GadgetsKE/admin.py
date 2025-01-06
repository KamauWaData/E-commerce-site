from django.contrib import admin
from .models import Customer, products, Cart
#, Payment,OrderPlaced

# Register your models here.
@admin.register(products)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discount', 'category', 'image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

#@admin.register(Payment)
#class PaymentModelAdmin(admin.ModelAdmin):
#    list_display = ['id','user','amount','razorpay_payment_status','razorpay_payment_id','razorpay_payment_id','paid']

#@admin.register(OrderPlaced)
#class OrderPlacedModelAdmin(admin.ModelAdmin):
#    list_display = ['id','user','customer','product','quantity','order_date','status','payment']