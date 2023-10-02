from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('inicio/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('tienda/', views.tienda, name="tienda"),
    path('evento/', views.evento, name="evento"),
    path('como_hacemos/', views.como_hacemos, name="como_hacemos"),
    path('aprender/', views.aprende, name="aprender"),
    path('acerca_de/', views.acerca_de, name="acerca_de"),
    path('acceso/', views.acceso, name="acceso"),
    path('registrate/', views.registrate, name="registrate"),
    path('comprar/', views.comprar, name="comprar"),
    path('success/', views.success, name='success'),
    path('terminos/', views.terminos, name='terminos'),
    path('error/', views.error, name='error'),
    path('pasarela_retorno/', views.pasarela_retorno, name='pasarela_retorno'),
]