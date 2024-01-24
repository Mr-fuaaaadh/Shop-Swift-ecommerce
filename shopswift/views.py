from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .models import Customer,Product,Cart,Orders
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from twilio.rest import Client
from django.conf import settings
# from django.db.models import Sum
from django.db.models import Q   # IMPORT DJANGO QUOERY SET 
import razorpay

# Create your views here.


# account login setting
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)
        # checking email and password is correct
        LoginData = Customer.objects.filter(coustomer_email=email, coustomer_password=password)
        print(LoginData)
        if LoginData:
            #checking in user already login in account  
            request.session['User'] = email
            return redirect('/')
        else:
            return render(request, 'login.html', {"status": "invalid"})
    return render(request, 'login.html')
def createAccount(request):
    if request.method == "POST":
        id = request.POST.get('id')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        usertype = request.POST.get('usertype')
        status = request.POST.get('status')
        ImportData = Customer()
        ImportData.coustomer_id = id
        ImportData.coustomer_email = email
        ImportData.coustomer_password = password
        ImportData.coustomer_usertype = usertype
        ImportData.coustomer_status = status
        ImportData.save()
    return render(request, 'create.html')



def index(request):
    if 'User' in request.session:
        return redirect('home/')
    else:
        return redirect('login/')


def logout(request):
    # clicking logout button delete session in this account
    del request.session['User']
    return redirect('login/')


def home(request):
    product_add =  Product.objects.all()
    print(product_add)
    return render (request, 'shopswift.html', {'product_add':product_add})

# admin adding in prodect in home page 
def AddProduct(request):
    product_add =  Product.objects.all()
    return render (request, 'shopswift.html', product_add)


def ViewProduct(request,id):
    if request.method == "POST":
        if "addcart" in request.POST:
            if 'User' in request.session:
                cart_add=Cart()
                # user favorite products adding in cart items
                LoginData = Customer.objects.get(coustomer_email=request.session['User'])
                cart_add.cart_user = LoginData
                cart_add.cart_product = Product.objects.get(product_id = id)
                cart_add.cart_product_amount = Product.objects.get(product_id = id)
                print(Product.objects.get(product_id = id))   # just checking for my use
                cart_add.cart_size = request.POST.get('size')
                cart_add.cart_quantity = 1
                cart_add.save()

                return redirect('/favorite')
        if "buy_product" in request.POST:
            if 'User' in request.session:
                order=Orders()
                user_data = Customer.objects.get(coustomer_email=request.session['User'])
                order.order_customer = user_data
                order.order_product = Product.objects.get(product_id = id)
                order.order_product_rate = Product.objects.get(product_id = id)
                print(Product.objects.get(product_id = id)) # just checking for my use
                order.order_product_size = request.POST.get("size")
                order.order_product_quantity = 1
                order.save()
                print(user_data,order)
            return redirect('/orders')
            # user selecte the product and viewing 
    print('myr',id)
    Buy = Product.objects.filter(product_id = id)
    print(Buy)
    return render(request, 'buy.html',{'buy' : Buy})


def AddToCart(request):
    # user favorite products adding in cart items
    if 'User' in request.session:
        LoginData = Customer.objects.get(coustomer_email=request.session['User'])
        fav_itmes = Cart.objects.filter(cart_user=LoginData)
        return render(request, 'favorite.html', {'fav_item': fav_itmes})
    else:
        return redirect('login/')


def cart_product_remove(request,id):
    remove_product =Cart.objects.get(id=id)
    remove_product.delete()
    print(remove_product)
    return redirect('/favorite',{"fav_item": remove_product})



# searching  product viewing 
def search_view(request):
    if request.method == 'POST':
        product = request.POST.get('values')
        if product:
            result = Product.objects.filter(product_name=product)
            
        else:
            result = Product.objects.all()
    return render( request,'search.html',{'buy' : result})

# Forgott password otp senting method
def forgot_password(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        check_number = Customer.objects.filter(coustomer_phone = phone_number)
        if check_number:
            print("phone number is correct   :")
        return render(request, 'otp.html')
    return render(request, 'reset.html')


#otp validation
def otp_validation(request):
    if request.method == 'POST':
        account_sid = "ACcde1c079410b83248d1a3dccbee5eac6"
        auth_token = "cfa3b2f61cc6cc275a8b20d27515be85"
        verify_sid = "VAf2eb3332d147cfcef3f48097b50f4815"
        verified_number = "+919645848527"
        client = Client(account_sid, auth_token)
        verification = client.verify.v2.services(verify_sid) \
            .verifications \
                .create(to=verified_number, channel="sms")
        print(verification.status)

        otp = request.POST.get('otp')

        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
                .create(to=verified_number, code=otp)
        print(verification_check.status)
        return HttpResponse("set myr")
    return render(request, 'otp.html')


def price_filitering(request):
    if request.method == 'POST' :
        price = request.POST.get('rate')
        price2 = request.POST.get('rate')
        check_data = Product.objects.filter(product_rate__gte = price, product_rate__lte=price2)
        if check_data :
            check_data = Product.objects.all()
        return render(request , 'filering.html'  ,{'check_data' : check_data})
    return render(request , 'filering.html')


def product_category(request, id):
    if id=="Formal_men":
        result = Product.objects.filter(product_category_id	=1)
        return render(request,'desktop.html',{"data":result})

    elif id == 'casual_men':
        result = Product.objects.filter(product_category_id	=2)
        return render(request,'desktop.html',{"data":result})

    elif id =="sports_men":
        result = Product.objects.filter(product_category_id	=3)
        return render(request,'desktop.html',{"data":result})

    elif id =="jacket_men":
        result = Product.objects.filter(product_category_id	=4)
        return render(request,'desktop.html',{"data":result})

    elif id =="jacket_men":
        result = Product.objects.filter(product_category_id	=4)
        return render(request,'desktop.html',{"data":result})

    elif id =="sunglasses_men":
        result = Product.objects.filter(product_category_id	=5)
        return render(request,'desktop.html',{"data":result})

    elif id =="Formal_women":
        result = Product.objects.filter(product_category_id	=6)
        return render(request,'desktop.html',{"data":result})

    elif id =="casual_woman":
        result = Product.objects.filter(product_category_id	=7)
        return render(request,'desktop.html',{"data":result})

    elif id =="Perfume_woman":
        result = Product.objects.filter(product_category_id	=8)
        return render(request,'desktop.html',{"data":result})

    elif id =="cosmetics_women":
        result = Product.objects.filter(product_category_id	=9)
        return render(request,'desktop.html',{"data":result})

    elif id =="bags_women":
        result = Product.objects.filter(product_category_id	=10)
        return render(request,'desktop.html',{"data":result})

    elif id =="Earrings":
        result = Product.objects.filter(product_category_id	= 11)
        return render(request,'desktop.html',{"data":result})

    elif id =="Couple_ring":
        result = Product.objects.filter(product_category_id	= 12)
        return render(request,'desktop.html',{"data":result})

    elif id =="Necklace":
        result = Product.objects.filter(product_category_id	= 13)
        return render(request,'desktop.html',{"data":result})

    elif id =="bracelets":
        result = Product.objects.filter(product_category_id	= 14)
        return render(request,'desktop.html',{"data":result})

    elif id =="Cloths_Persume":
        result = Product.objects.filter(product_category_id	= 15)
        return render(request,'desktop.html',{"data":result})

    elif id =="Deodorant":
        result = Product.objects.filter(product_category_id	= 16)
        return render(request,'desktop.html',{"data":result})

    elif id =="Flower_fragrance":
        result = Product.objects.filter(product_category_id	= 17)
        return render(request,'desktop.html',{"data":result})

    elif id =="air_freshener":
        result = Product.objects.filter(product_category_id	= 18)
        return render(request,'desktop.html',{"data":result})

    elif id =="phone":
        result = Product.objects.filter(product_category_id	= 19)
        return render(request,'desktop.html',{"data":result})

    elif id =="computer":
        result = Product.objects.filter(product_category_id	= 20)
        return render(request,'desktop.html',{"data":result})

    elif id =="tabe":
        result = Product.objects.filter(product_category_id	= 21)
        return render(request,'desktop.html',{"data":result})

    elif id =="Watch":
        result = Product.objects.filter(product_category_id	= 22)
        return render(request,'desktop.html',{"data":result})
    
    elif id =="Speaker":
        result = Product.objects.filter(product_category_id	= 23)
        return render(request,'desktop.html',{"data":result})
   
    return render(request,'desktop.html')

def order_product(request):
     # user favorite products adding in cart items
    if 'User' in request.session:
        print("KL")
        user_data = Customer.objects.get(coustomer_email=request.session['User'])
        fav_itmes = Orders.objects.filter(order_customer = user_data)
        print("KL")
        sum=0
        for iteam in fav_itmes:
            sum=sum+int(iteam.order_product.product_rate)
            print(iteam.order_product.product_rate )
        sum1=str(sum)+"00"
        print("sum is ",float(sum) )

        return render(request, 'shope.html', {'fav_item': fav_itmes,'sum':sum,"sum1":sum1})
    else:
        return redirect('login/')

    return render(request, 'shope.html') 

def order_product_remove(request,id):
    order_remove = Orders.objects.get(id=id)
    order_remove.delete()
    return redirect('/orders',{"fav_item" : order_remove })


def order_successfull(request,id):
    if request.method == 'POST':  
        if 'checkout' in request.POST :
            order_confirm = OrderPaymentConfirm()
            LoginData = Customer.objects.get(coustomer_email=request.session['User'])
            order_confirm.User = LoginData
            order_confirm.amount = Orders.objects.get(id = id)
            order_confirm.razorpay_order_id = 250
            order_confirm.Razorpay_payment_status = phonepay
            order_confirm.Razorpay_payment_id = 2
            order_confirm.paid = request.POST.get('rate')
            order_confirm.save()
            print('sndi',order_confirm)

    return redirect('/orders') 
    


   











# def admin(request):
    return render(request, 'admin.html')



# def sellers(request):
#     return render(request, 'sellers.html')



# def prp(request):
    
#     return  render(request , 'index.html')