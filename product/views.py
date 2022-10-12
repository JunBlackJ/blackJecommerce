from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from product.models import *
from django.contrib import messages
from home.models import *
from order.models import *



def index(request):
	setting = Setting.objects.get(pk=1)
	category = Category.objects.all()
	product = Product.objects.all()
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	ranked = Product.objects.all().order_by('?')[:6]
	#shipping = 0
	#for rs in shopcart:
		#shipping = float(2000)
	subtotal=0
	for rs in shopcart:
		subtotal += rs.product.price * rs.quantity
	total=0
	for rs in shopcart:
		total += rs.product.price * rs.quantity
	added=0
	for rs in shopcart:
		added +=  rs.quantity
	context = {'setting':setting, 'category':category, 
				'product':product,
				#'shipping':shipping,
				'total':total,
				'added':added, 
				'ranked':ranked,
				'shopcart':shopcart,
				}
	return render(request, "product.html", context)

def addcomment(request, id):
	url = request.META.get('HTTP_REFERER')
	#return HttpResponse(url)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			data = Comment()
			data.subject = form.cleaned_data['subject']
			data.comment = form.cleaned_data['comment']
			data.rate = form.cleaned_data['rate']
			data.ip = request.META.get('REMOTE_ADDR')
			data.product_id = id
			current_user = request.user
			data.user_id = current_user.id
			data.save()
			messages.success(request, "Your product review was delivered. thanks for your patronage")
			return HttpResponseRedirect(url)

	return HttpResponseRedirect(url)