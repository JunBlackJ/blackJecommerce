from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from product.models import Category, Product, Images, Comment
from home.models import Setting, ContactForm, ContactMessage
from home.forms import SearchForm
from order.models import ShopCart, ShopCartForm
import json
# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    products_slider = Product.objects.all().order_by('?')[:6]
    products_latest = Product.objects.all().order_by('-id')[:6]
    products_daily = Product.objects.all().order_by('id')[:6]
    products_picked = Product.objects.all().order_by('?')[:6]
    one_picked = Product.objects.all().order_by('?')[:1]
    latest = Product.objects.all().order_by('?')[:1]
    page = "home"
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
    context = {'setting':setting,
            'page':page, 
            'category':category,
            'products_slider':products_slider,
            'products_latest': products_latest,
            'products_daily': products_daily,
            'products_picked': products_picked,
            'one_picked':one_picked,
            'latest':latest,
            'total':total,
            'subtotal':subtotal,
            'added': added,
            'shopcart':shopcart,
            }
    return render(request, 'index.html', context)

def aboutus(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

   # shipping = 0
    #for rs in shopcart:
       # shipping = float(2000)

    subtotal=0
    for rs in shopcart:
        subtotal += rs.product.price * rs.quantity

    total=0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    added=0
    for rs in shopcart:
        added +=  rs.quantity
    context = {'setting':setting,
                'category': category,
                'total':total,
                'added':added,
                'subtotal':subtotal,
                'shopcart':shopcart,
                    }
    return render(request, 'about.html', context)

def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message was delivered")
            return HttpResponseRedirect('/contact')
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    total=0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    added=0
    for rs in shopcart:
        added +=  rs.quantity
    context = {'setting':setting, 
                'total':total, 
                'added':added, 
                'form':form, 
                'category':category,
                'shopcart':shopcart,
                }
    return render(request, 'contact.html', context)

def category_products(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    products = Product.objects.filter(category_id=id)
    catdata = Category.objects.get(pk=id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    total=0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    added=0
    for rs in shopcart:
        added +=  rs.quantity
    context = {
            'setting':setting,
            'total':total,
            'added':added,
            'products':products,
            'category':category,
            'catdata':catdata,
            'shopcart':shopcart,
            }
    return render(request, 'category_products.html', context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products=Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            current_user = request.user
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
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
            context = {'products':products,
                        'query':query,
                        'added':added,
                        'total':total,
                        'subtotal':subtotal,
                        'category':category,
                        'setting':setting,
                        'shopcart':shopcart,
                        }

            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    products = Product.objects.filter(title__icontains=q)
    results = []
    for rs in products:
      products_json = {}
      products_json = rs.title
      results.append(products_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def product_detail(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    product = Product.objects.get(pk=id)
    products_picked = Product.objects.all().order_by('?')[:4]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    #shipping = 0
    #for rs in shopcart:
       # shipping = float(2000)

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
            'setting':setting,
            'product':product,
            'products_picked': products_picked,
            'category':category,
            'images':images,
            'comments':comments,
            'total':total,
            'added':added,
            'shopcart':shopcart,
            }
    return render(request, 'product_detail.html', context)


