from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category, Comment
from django.contrib.auth import authenticate, login, logout
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from order.models import *
from user.models import UserProfile
from home.models import *
from django.conf import settings
from django.core.mail import send_mail
from order.models import Order, OrderProduct
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
@login_required(login_url='/login')
def  index(request):
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	profile = UserProfile.objects.get(user_id=current_user.id)
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
	context = {'category': category,
				'profile':profile,
				'total':total,
				'added':added,
				'shopcart':shopcart,
				'setting':setting,
				}
	return render(request, 'user_profile.html', context)

def login_form(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "welcome "+user.username)
			current_user = request.user
			userprofile = UserProfile.objects.get(user_id = current_user.id)
			request.session['userimage'] = userprofile.image.url
			return HttpResponseRedirect('/')
		else:
			messages.warning(request, "Login Error !! username or password is incorrect")
			return HttpResponseRedirect('/login')
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	total=0
	for rs in shopcart:
		total += rs.product.price * rs.quantity
	added=0
	for rs in shopcart:
		added +=  rs.quantity
	context = {
		'category':category,
		'total':total,
		'added':added,
		'shopcart':shopcart,
		'setting':setting,
	}
	return render(request, 'login_form.html', context)

def signup_form(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			email = form.cleaned_data.get('email')
			phone = form.cleaned_data.get('phone')
			user = authenticate(username=username, password=password)
			login(request, user)
			current_user = request.user
			data = UserProfile()
			data.user_id = current_user.id

			data.image="images.png"
			data.save()
			messages.success(request, 'Account successfully created')
			return HttpResponseRedirect('/')
		else:
			messages.warning(request, form.errors)
			return HttpResponseRedirect('/signup')
	form = SignUpForm()
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)

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
	context = {'category': category,
				'form':form,
				'total':total,
				'added':added,
				'subtotal':subtotal,
				'shopcart':shopcart,
				'setting':setting,
				}
	return render(request, 'signup_form.html', context)

def logout_func(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/login')
def user_update(request):
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your account has been successfully updated')
			return HttpResponseRedirect('/user')
	else:
		category = Category.objects.all()
		setting = Setting.objects.get(pk=1)
		user_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user.userprofile)
		current_user = request.user
		shopcart = ShopCart.objects.filter(user_id=current_user.id)

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
		context = {
			'category':category,
			'total':total,
			'added':added,
			'user_form':user_form,
			'profile_form': profile_form,
			'shopcart':shopcart,
			'setting':setting,
		}
		return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
	form = PasswordChangeForm(request.user, request.POST)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your Password was successfully changed')
			return HttpResponseRedirect('/user')
		else:
			messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
			return HttpResponseRedirect('/user/password')
	else:
		setting = Setting.objects.get(pk=1)
		category = Category.objects.all()
		current_user = request.user
		shopcart = ShopCart.objects.filter(user_id=current_user.id)
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

		form = PasswordChangeForm(request.user)
		return render(request, 'user_password.html', {
			'form':form,
			'total':total,
			'added':added, 
			'category':category,
			'shopcart':shopcart,
			'setting':setting,
			})
@login_required(login_url='/login')
def user_orders(request):
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	orders = Order.objects.filter(user_id=current_user.id)
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
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

	context = {'category':category,
				'orders': orders,
				'total': total,
				'added': added,
				'setting':setting,
	}
	return render(request, 'user_orders.html', context)

@login_required(login_url='/login')
def user_orderdetail(request, id):
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
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

	order = Order.objects.get(user_id=current_user.id, id=id)
	orderitems = OrderProduct.objects.filter(order_id=id)
	context={
		'category':category,
		'order': order,
		'total': total,
		'added': added,
		'orderitems':orderitems,
		'shopcart':shopcart,
		'setting':setting,
	}
	return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login')
def user_orders_product(request):
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
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

	order_product = OrderProduct.objects.filter(user_id=current_user.id)
	context = {'category':category,
				'added':added,
				'total':total,
				'order_product': order_product,
				'shopcart':shopcart
	}
	return render(request, 'user_orders_product.html', context)

@login_required(login_url='/login')
def  user_order_product_detail(request, id, oid):
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
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

	order = Order.objects.get(user_id=current_user.id, id=oid)
	orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
	context={
		'category':category,
		'order': order,
		'orderitems':orderitems,
		'total':total,
		'added':added,
		'shopcart':shopcart,
		'setting':setting,
	}
	return render(request, 'user_order_detail.html', context)

def user_comments(request):
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
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

	comments = Comment.objects.filter(user_id=current_user.id)
	context={
		'category':category,
		'comments': comments,
		'total':total,
		'added':added,
		'shopcart':shopcart,
		'setting':setting,
	}
	return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomment(request, id):
	current_user = request.user
	comments = Comment.objects.filter(id=id, user_id=current_user.id).delete()
	messages.success(request, 'Comment deleted..')
	return HttpResponseRedirect('/user/comments')

def faq(request):
	category = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
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

	faq = FAQ.objects.filter(status="True").order_by("ordernumber")
	context={
		'category':category,
		'faq': faq,
		'total':total,
		'added':added,
		'shopcart':shopcart,
		'setting':setting,
	}
	return render(request, 'faq.html', context)



