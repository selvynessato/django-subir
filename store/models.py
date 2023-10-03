from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True)  # Campo para identificar de manera única cada imagen
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='galeria/')
    descripcion = models.TextField(blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    tipo_imagen = models.CharField(max_length=50)  # Campo para especificar el tipo de imagen

    def __str__(self):
        return self.titulo

class Pais(models.Model):
    id_pais = models.IntegerField(primary_key=True)
    nombre_pais = models.CharField(max_length=150)


class EstaDepto(models.Model):
    id_esta_depto = models.IntegerField(primary_key=True)
    nombre_esta_depto = models.CharField(max_length=150)
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE)


class Munici(models.Model):
    id_munici = models.IntegerField(primary_key=True)
    nombre_munici = models.CharField(max_length=150)
    id_esta_depto = models.ForeignKey(EstaDepto, on_delete=models.CASCADE)

class Pedido(models.Model):
    x_login = models.CharField(max_length=255)
    x_api_key = models.CharField(max_length=255)
    x_amount = models.DecimalField(max_digits=10, decimal_places=2)
    x_currency_code = models.CharField(max_length=3)
    x_first_name = models.CharField(max_length=255)
    x_last_name = models.CharField(max_length=255)
    x_phone = models.CharField(max_length=20)
    x_ship_to_address = models.TextField()
    x_ship_to_city = models.CharField(max_length=255)
    x_ship_to_country = models.CharField(max_length=255)
    x_ship_to_state = models.CharField(max_length=255)
    x_ship_to_zip = models.CharField(max_length=10)
    x_ship_to_phone = models.CharField(max_length=20)
    x_description = models.TextField()
    x_url_success = models.URLField()
    x_url_error = models.URLField()
    x_url_cancel = models.URLField()
    http_origin = models.URLField()
    x_company = models.CharField(max_length=255)
    x_address = models.TextField()
    x_city = models.CharField(max_length=255)
    x_country = models.CharField(max_length=255)
    x_state = models.CharField(max_length=255)
    x_zip = models.CharField(max_length=10)
    x_freight = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2)
    x_email = models.EmailField()
    x_type = models.CharField(max_length=20)
    x_method = models.CharField(max_length=20)
    x_invoice_num = models.CharField(max_length=20)
    custom_fields = models.JSONField()
    x_visacuotas = models.CharField(max_length=10)
    x_relay_url = models.URLField()
    origen = models.CharField(max_length=255)
    store_type = models.CharField(max_length=255)
    x_discount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'store_pedido'

    def __str__(self):
        return f"Pedido #{self.id}"
