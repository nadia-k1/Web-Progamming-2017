from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext, loader
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Product, Cart
from rest_framework import viewsets
from .serializers import ProfileSerializer, ProductSerializer, CartSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

def login_view(request):
	context = {}

	if(request.method == 'POST'):
		u = request.POST.get('username')
		p = request.POST.get('password')

		if(u is "" or p is ""):
			context['error'] = "Error! Please enter a value in each field."
		else:
			user = authenticate(username=u, password=p)
			if user is not None:
				login(request, user)
				request.session['username'] = u
				return HttpResponseRedirect('/shoeshop/products')
			else:
				context['error'] = "Error! Invalid login."

	return render(request, "shoeshop/login_view.html", context)

def logout_view(request):
	logout(request)
	request.session.flush()
	return HttpResponseRedirect('/shoeshop')

def register(request):
	context = {}

	if(request.method == 'POST'):
		f = request.POST['fName']
		l = request.POST['lName']
		e = request.POST['email']
		u = request.POST['username']
		ph = request.POST['phone']
		a = request.POST['address']
		p = request.POST['password']
		cp = request.POST['confirmPassword']

		if(f is "" or l is "" or e is "" or u is "" or ph is "" or a is "" or p is "" or cp is ""):
			context['error'] = "Error! Please enter a value in each field."
		elif(p != cp):
			context['error'] = "Error! Password do not match."
		else:
			Users = User.objects.all()
			for user in Users:
				if(user.email==e):
					context['error'] = "Error! Email address already exists."
				else:
					u = User.objects.create_user(first_name=f, last_name=l, email=e, username=u, password=p)
					u.profile.phone = ph
					u.profile.address = a
					u.save()
					return HttpResponseRedirect('/shoeshop')

	return render(request, 'shoeshop/register.html', context)

def products(request):
	products = Product.objects.all()

	if 'username' in request.session:
		username = request.session['username']
		user = User.objects.get(username=username)

		if 'add' in request.GET:
			product = request.GET['add']
			product_obj = Product.objects.get(pk=product)
			cart = Cart(user.id,product_obj.id,1,100.0)
			cart.save()


	return render(request, "shoeshop/products.html", {'Products':products})

def cart(request):
	context = {}

	if 'username' in request.session:
		username = request.session['username']
		user_obj = User.objects.get(username=username)

		cart = Cart.objects.get(user_id=user_obj)
		for cart_obj in cart:
			product = cart_obj.product
			context['Cart'] = product

	#cart = user.cart
	#cart_obj = Cart.objects.get[pk=username]
	#email = request.session['email_address']
	#user = User.objects.get(pk=email)
	#cart = user.cart.objects.all()

	#if 'remove' in request.GET:
		#product = request.GET['remove']
		#product_obj = Product.objects.get(pk=product)
		#Cart.objects.filter(cartproduct=product_obj).delete()

	return render(request, "shoeshop/cart.html", context)


'''
send_mail('Password reminder',
		  'Your password is...',
		  'app_email@server.com',
		  ['user1@gmail.com','user2@gmail.com'],
		  fail_silently=False)'''