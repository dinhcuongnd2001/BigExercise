from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
import json
import datetime
from .models import *
from .utils import cookieCart,cartData, guestOrder
from .forms import RegistrationForm, ReviewForm, UpdateProfileForm,UpdateUserForm
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
def infoUser(customer):
    infomations = []
    info = {
        'customer': {
            'full_name':customer.user.get_full_name(),
            'user':customer.user,
            'name':customer.name,
            'email':customer.user.email,
            'phone':customer.phone,
            'imageURL':customer.imageURL,
        },
    }
    infomations.append(info)
    return infomations

@login_required(login_url='login')
def profile(request):
    context = {}
    customer = Customer.objects.get(user=request.user)
    print(customer)
    print(infoUser(customer))
    context = {'info':infoUser(customer)}
    return render(request,'store/profile.html',context)


def profile_update(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm( request.POST,request.FILES, instance=request.user.customer)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save() 
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.customer)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'info':infoUser(customer),
    }
    return render(request,'store/profile_update.html',context)


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'You have successfully registered an account!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request,'store/register.html',{'form':form})

def store(request):
    search_post = request.GET.get('search')
    products = Product.objects.all() 
    if search_post:
        products = Product.objects.filter(Q(name__contains=search_post))
    else:
        products = Product.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']

    
    context = {'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)


def product_detail(request):
    data = cartData(request)
    cartItems = data['cartItems']
    product = request.GET
    items = []
    reviews = Review.objects.all()
    for i in product.items():
        try:
            product = Product.objects.get(id=i[0])
            item = {
                'product': {
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    'description':product.description,
                },
            }
            items.append(item)
        except:
            pass
    listReview = {}
    for i in reviews:
        if i.product.id not in listReview:
            listReview[i.product.id] = 1
        else:
            listReview[i.product.id] += 1
    # print(listReview)
    context = {'Items':items,'cartItems':cartItems,'reviews':reviews,'listReview':listReview}
    return render(request,'store/product_detail.html',context)
    # return JsonResponse(request.GET, safe=False)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


def updateItem(request):
    # data = json.loads(request.data)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was added", safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()
    
	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = Review()
            data.comment= form.cleaned_data['comment']
            data.rate= form.cleaned_data['rate']
            data.product_id = product_id
            data.user_id = request.user.id
            data.save()                
            print(data)
                # messages.success(request,"Thank you! Your reviews has been submited.")
            return redirect(url)