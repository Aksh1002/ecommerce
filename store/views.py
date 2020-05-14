from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
import datetime
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import json
# Create your views here.
def store(request):

	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartitems=order.get_cart_item
	else:
		items=[]
		order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
		cartitems=order['get_cart_item']


	products=Product.objects.all()
	context={'products':products,'cartitems':cartitems}
	return render(request,'store/store.html',context)
    


def cart(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartitems=order.get_cart_item
	else:
		items=[]
		order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
		cartitems=order['get_cart_item']
	context={'items':items,'order':order,'cartitems':cartitems}	
	return render(request,'store/cart.html',context)


def checkout(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartitems=order.get_cart_item
	else:
		items=[]
		order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
		cartitems=order['get_cart_item']
	context={'items':items,'order':order,'cartitems':cartitems}	
	return render(request,'store/checkout.html',context)


def updateItem(request):
	data=json.loads(request.body)
	productID=data['productID']
	action=data['action']
	print('action:',action)
	print('Product:',productID)

	customer=request.user.customer
	product=Product.objects.get(id=productID)
	order,created=Order.objects.get_or_create(customer=customer,complete=False)
	orderitem,created=OrderItem.objects.get_or_create(order=order,product=product)

	if action=="add":
		orderitem.quantity=(orderitem.quantity+1)
	elif action=="remove":
		orderitem.quantity=(orderitem.quantity-1)
	
	orderitem.save()
	if orderitem.quantity<=0:
		orderitem.delete()

	return JsonResponse("data added",safe=False)
		


def processorder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		total=float(data['form']['total'])
		order.transaction_id=transaction_id

		if total==order.get_cart_total:
			order.complete=True
		order.save()
		subject="Thank You for your order"
		message=" Your order is confirmed,your order id is"+str(transaction_id)
		from_email=settings.EMAIL_HOST_USER
		to_list=[data['form']['email']]
		send_mail(subject,message,from_email,to_list,fail_silently=False)

		if order.shipping==True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print("user not logged")
	
	return JsonResponse("data added",safe=False)