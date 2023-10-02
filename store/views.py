from store.models import Product
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
import requests
from .utils import cookieCart, cartData, guestOrder
from decimal import Decimal
from django.contrib import messages
import logging




url = "https://payments.qpaypro.com/checkout/register_transaction_store"
#url = "https://sandboxpayments.qpaypro.com/checkout/register_transaction_store"


def error(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}

    return render(request,'store/error.html', context)

def success(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}

    return render(request,'store/success.html', context)

def terminos(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}

    return render(request,'store/terminos.html', context)

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

    return JsonResponse('Producto agregado', safe=False)

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

    if total == order.get_cart_total():
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

	data = cartData(request)

	cartItems =data['cartItems']
	order = data['order']
	items = data['items']

	context ={'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/comoHacemos.html', context)

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

def pasarela_retorno(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    total_pedido = order['get_cart_total']
    total_pedido_str = f"{order['get_cart_total']:.2f}"
    cantidad_articulos = order['get_cart_items']
    nombres_cantidad_productos = [f"{item['product']['name']}={item['quantity']}" for item in items]

    # Procesar la respuesta de la pasarela de pagos
    if request.method == 'GET':
        # Extraer los datos relevantes de la respuesta
        x_login = request.GET.get('x_login', '')
        x_api_key = request.GET.get('x_api_key', '')
        x_amount = float(request.GET.get('x_amount', 0.0))
        x_currency_code = request.GET.get('x_currency_code', '')
        x_first_name = request.POST.get('nombre')
        x_last_name = request.GET.get('x_last_name', '')
        x_phone = request.GET.get('x_phone', '')
        x_ship_to_address = request.GET.get('x_ship_to_address', '')
        x_ship_to_city = request.GET.get('x_ship_to_city', '')
        x_ship_to_country = request.GET.get('x_ship_to_country', '')
        x_ship_to_state = request.GET.get('x_ship_to_state', '')
        x_ship_to_zip = request.GET.get('x_ship_to_zip', '')
        x_ship_to_phone = request.GET.get('x_ship_to_phone', '')
        x_description = ", ".join(nombres_cantidad_productos)
        x_url_success = request.GET.get('x_url_success', '')
        x_url_error = request.GET.get('x_url_error', '')
        x_url_cancel = request.GET.get('x_url_cancel', '')
        http_origin = request.GET.get('http_origin', '')
        x_company = request.GET.get('x_company', '')
        x_address = request.GET.get('x_address', '')
        x_city = request.GET.get('x_city', '')
        x_country = request.GET.get('x_country', '')
        x_state = request.GET.get('x_state', '')
        x_zip = request.GET.get('x_zip', '')
        x_freight = float(request.GET.get('x_freight', 0.0))
        taxes = float(request.GET.get('taxes', 0.0))
        x_email = request.GET.get('x_email', '')
        x_type = request.GET.get('x_type', '')
        x_method = request.GET.get('x_method', '')
        x_invoice_num = request.GET.get('x_invoice_num', '')
        custom_fields = request.GET.get('custom_fields', '')
        x_visacuotas = request.GET.get('x_visacuotas', '')
        x_relay_url = request.GET.get('x_relay_url', '')
        origen = request.GET.get('origen', '')
        store_type = request.GET.get('store_type', '')
        x_discount = float(request.GET.get('x_discount', 0.0))

        # Crear una instancia del modelo Pedido y guardar los datos en la base de datos
        pedido = Pedido(
            x_login=x_login,
            x_api_key=x_api_key,
            x_amount=x_amount,
            x_currency_code=x_currency_code,
            x_first_name=x_first_name,
            x_last_name=x_last_name,
            x_phone=x_phone,
            x_ship_to_address=x_ship_to_address,
            x_ship_to_city=x_ship_to_city,
            x_ship_to_country=x_ship_to_country,
            x_ship_to_state=x_ship_to_state,
            x_ship_to_zip=x_ship_to_zip,
            x_ship_to_phone=x_ship_to_phone,
            x_description=x_description,  # Usar el valor modificado
            x_url_success=x_url_success,
            x_url_error=x_url_error,
            x_url_cancel=x_url_cancel,
            http_origin=http_origin,
            x_company=x_company,
            x_address=x_address,
            x_city=x_city,
            x_country=x_country,
            x_state=x_state,
            x_zip=x_zip,
            x_freight=x_freight,
            taxes=taxes,
            x_email=x_email,
            x_type=x_type,
            x_method=x_method,
            x_invoice_num=x_invoice_num,
            custom_fields=custom_fields,
            x_visacuotas=x_visacuotas,
            x_relay_url=x_relay_url,
            origen=origen,
            store_type=store_type,
            x_discount=x_discount,
        )

        pedido.save()

        context = {
            'items': items,
            'order': order,
            'cartItems': cartItems,
            #'paises': paises,  # Agregamos paises al contexto
            #'estadeptos': estadeptos  # Agregamos estadeptos al contexto
        }
        # Redirigir al usuario a una página de confirmación u otra página relevante
        return redirect('success')



    # Manejar otros casos, como respuestas POST, de acuerdo con tus necesidades
    return HttpResponse('Procesamiento de respuesta de pasarela de pagos')

    
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    paises = Pais.objects.all()
    estadeptos = EstaDepto.objects.all()

    total_pedido = order['get_cart_total']
    total_pedido_str = f"{order['get_cart_total']:.2f}"
    cantidad_articulos = order['get_cart_items']

    nombres_cantidad_productos = [f"{item['product']['name']}={item['quantity']}" for item in items]

    if cantidad_articulos > 9 or cantidad_articulos == 0:
        descuento = 25
    else:    
        descuento = 0
        

    if request.method == 'POST':
        headers = {
            "Content-Type": "application/json"
        }

        pais = request.POST.get('pais', '')  # País principal
        departamento = request.POST.get('departamento', '')  # Departamento principal
        municipio = request.POST.get('municipio', '')  # Municipio principal

        pais_envio = request.POST.get('paisEnvio', '')  # País de envío
        departamento_envio = request.POST.get('departamentoEnvio', '')  # Departamento de envío

        nit = request.POST.get('nit', '')

        x_company = "C/F" if nit == "" or nit == "0" else nit

            

            #"x_login": "visanetgt_qpay",
            #"x_api_key": "88888888888",    
        
        payload = {    
            "x_login": "J4O2kCK36rgp3803",
            "x_api_key": "vmRDbmOJ0VE73803",
            "x_api_secret": "lWpeVyhUaMS43803",
            "x_amount": str(total_pedido_str),
            "x_currency_code": "GTQ",
            "x_first_name": request.POST.get('nombre'),
            "x_last_name": request.POST.get('apellido'),
            "x_phone": request.POST.get('telefono'),
            "x_ship_to_address": request.POST.get('direccion_envio', ''),
            "x_ship_to_city": request.POST.get('muni_envio', ''),
            "x_ship_to_country": "Guatemala",
            "x_ship_to_state": departamento_envio,
            "x_ship_to_zip": "0000",
            "x_ship_to_phone": request.POST.get('telefono', ''),
            "x_description": ", ".join(nombres_cantidad_productos),
            "x_url_success": "http://192.168.0.17:8000/pasarela_retorno/",  # Completa con la URL de éxito
            "x_url_error": "http://192.168.0.17:8000/error/",  # Completa con la URL de error
            "x_url_cancel": "http://192.168.0.17:8000/checkout/",  # Completa con la URL de cancelación
            "http_origin": "http://192.168.0.17:8000",
            "x_company": x_company,
            "x_address": request.POST.get('direccion', ''),
            "x_city": municipio,
            "x_country": "Guatemala",
            "x_state": departamento,
            "x_zip": "0000",
            "products": [
                [
                    ", ".join(nombres_cantidad_productos),
                    "",
                    "",
                    "1",
                    total_pedido_str,
                    "1"
                ]
            ],
            "x_freight": "25.00",
            "taxes": "0.00",
            "x_email": request.POST.get('correo', ''),
            "x_type": "AUTH_ONLY",
            "x_method": "CC",
            "x_invoice_num": "123",
            "custom_fields": "{\"idSistema\": \"1009\",\"idCliente\": \"2025\",\"numerodeorden\":\"2585\"}",
            "x_visacuotas": "no",
            "origen": "PLUGIN",
            "x_relay_url": "http://192.168.0.17:8000/pasarela_retorno/",  
            "store_type": "hostedpage",
            "x_discount": descuento
        }
            
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        token = response_data.get("data", {}).get("token", "")
        redirect_url = f"https://payments.qpaypro.com/checkout/store?token={token}"

        # Redirige directamente a la pasarela de pagos
        return redirect(redirect_url)

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'paises': paises,  # Agregamos paises al contexto
        'estadeptos': estadeptos  # Agregamos estadeptos al contexto
    }

    return render(request, 'store/checkout.html', context)


