from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES =(
    ('KMB','Kiambu'),
    ('NRB','Nairobi'),
    ('MSA','Mombasa'),
    ('TVT','Taita Taveta'),
    ('KLF','Kilifi'),
    ('LMU','Lamu'),
    ('KSI','Kisii'),
    ('ELD','Eldoret'),
    ('KRC','Kericho'),
    ('KSM','Kisumu'),
    ('HMB','Homa Bay'),
    ('MCK','Machakos'),
    ('MK','Makueni'),
    ('KJD','Kajiado'),
    ('NRK','Narok'),
    ('MRSB','Marsabit'),
    ('TRK','Turkana'),
    ('MDR','Mandera')
)
CATEGORY_CHOICES={
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('LS', 'Lassi'),
    ('MS', 'Milkshake'),
    ('PN', 'Paneer'),
    ('GH', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice-Creams'),
}

class products(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField
    discount = models.FloatField()
    composition = models.TextField(default="")
    prodapp = models.TextField(default="")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    image = models.ImageField(upload_to="product")

    def __str__(self):
        return self.title
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

#class Payment(models.Model):
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    #amount = models.FloatField()
    #razorpay_order_id = models.Charfield(max_length=100, blank=True,null=True)
    #razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    #razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    #paid = models.BooleanField(default=False)

#class OrderPlaced(models.Model):
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    #customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    #product = models.ForeignKey(products,on_delete=models.CASCADE)
    #quantity = models.PositiveIntegerField(default=1)
    #order_date = models.DateTimeField(auto_now_add=True)
    #status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    #payment = models.ForeignKey(Payment, on_delete=models.CASCADE,default='')
    #@property
    #def total_cost(self):
        #return self.quantity * self.product.discount