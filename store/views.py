from store.models import Product
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)
    

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	
    if action == 'add':
    	orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
    	orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
    	orderItem.delete()

    return JsonResponse('Item was added', safe=False)

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

	if total == order.get_cart_total:
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

def tienda(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

	
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/tienda.html',context)
  
def evento(request):

    return render(request, 'store/evento.html')

def como_hacemos(request):

	imagens = Imagen.objects.all()

	return render(request, "store/comoHacemos.html",{
		'imagens': imagens
	})

def aprende(request):
    return render(request,"store/aprender.html")

def acerca_de(request):

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context ={'products':products, 'cartItems':cartItems}
	return render(request, 'store/acercaDe.html',context)


def acceso(request):
    return render(request,"store/acceso.html")

def registrate(request):
    return render(request,"store/registrate.html")

def comprar(request):
	return render(request,"store/comprar.html")

def lista_paises(request):
    return render(request,"store/lista_paises.html")

def charge(request):

	if request.method == 'POST':
		print('Data:', request.POST)

		amount = int(request.POST['amount'])

	customer = stripe.Customer.create(
		email=request.POST['email'],
		name=request.POST['nombre'],
		source=request.POST['stripeToken']
		)

	charge = stripe.Charge.create(
 	 	customer=customer,
 	 	amount=amount*100,
  		currency='usd',
  		description="Cafe"
	)

	return redirect(reverse('success', args=[amount]))

def successMsg(request, args):
	amount = args
	return render(request, 'base/success.html', {'amount':amount})

