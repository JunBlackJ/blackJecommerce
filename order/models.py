from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput
from product.models import Product

# Create your models here.
class ShopCart(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField()

	def __str__(self):
		return self.product.title

	@property
	def price(self):
		return (self.product.price)

	@property
	def amount(self):
		return (self.quantity * self.product.price)

class ShopCartForm(ModelForm):
	class Meta:
		model = ShopCart
		fields = ['quantity']

class Order(models.Model):
	STATUS = (
			('New', 'New'),
			('Accepted', 'Accepted'),
			('Preapparing', 'Preapparing'),
			('OnShipping', 'OnShipping'),
			('Completed', 'Completed'),
			('Cancelled', 'Cancelled'),
		)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	code = models.CharField(max_length=5, editable=False)
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	phone = models.CharField(blank=True, max_length=25)
	address = models.CharField(blank=True, max_length=150)
	city = models.CharField(blank=True, max_length=25)
	total=models.FloatField()
	status = models.CharField(max_length=15, choices=STATUS, default='New')
	ip = models.CharField(blank=True, max_length=25)
	adminnote = models.CharField(blank=True ,max_length=125)
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.user.first_name

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['first_name', 'last_name', 'address', 'phone', 'city']


class OrderProduct(models.Model):
	STATUS = (
		('New', 'New'),
		('Accepted', 'Accepted'),
		('Cancelled', 'Cancelled'),
		)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	price = models.FloatField()
	amount = models.FloatField()
	status = models.CharField(max_length=15, choices=STATUS, default='New')
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.product.title
			
