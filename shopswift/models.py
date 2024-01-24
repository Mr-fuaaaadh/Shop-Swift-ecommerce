from django.db import models
import datetime

# Create your models here.

class Customer(models.Model):
    coustomer_id = models.IntegerField(primary_key=True)
    coustomer_email = models.CharField(max_length=100,null=True)
    coustomer_password =  models.CharField(max_length=100,null=True)
    coustomer_phone = models.CharField(max_length=255,null=True)
    coustomer_place = models.CharField(max_length=255,null=True)
    otp = models.CharField(max_length=100,null=True)


class Category(models.Model): 
    Category_name = models.CharField(max_length=50) 
    
    def __str__(self): 
        return self.Category_name 

# product details
class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100,null=True)
    product_description = models.CharField(max_length=100,null=True)
    product_rate = models.CharField(max_length=200)
    product_stock = models.IntegerField(null=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to="images")


# cart details
class Cart(models.Model):
    cart_user = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    cart_product= models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    cart_size = models.CharField(max_length=100, null=True)
    cart_quantity = models.IntegerField()
    cart_product_amount = models.CharField(max_length=100,null=True)


# Product Orders
class Orders(models.Model):
    order_customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    order_product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    order_product_rate = models.CharField(max_length=100,null=True)
    order_product_size = models.CharField(max_length=100,null=True)
    order_product_quantity = models.IntegerField()
    order_date = models.DateField(default=datetime.datetime.today,null=True) 


class OrderPaymentConfirm(models.Model):
    User = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount= models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    Razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    Razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)






