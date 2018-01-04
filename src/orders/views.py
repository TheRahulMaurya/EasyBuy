import time
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from carts.models import Cart
from carts.models import Cart

from .models import Order

def order(request):
	context={}
	template = "orders/user.html"
	return render(request, template, context)

#require user login
@login_required
def checkout(request):
	try:
		the_id=request.session["cart_id"]
		cart= Cart.objects.get(id=the_id)
	except:
		the_id = None
		return HttpResponseRedirect(reverse("view_cart"))

	try:
		new_order = Order.objects.get(cart=cart)
	except Order.DoesNotExist:
		new_order = Order()
		new_order.cart=cart
		new_order.user = request.user
		new_order.order_id = str(time.time())
		new_order.save()
	except:
		#work on some error  message
		return HttpResponseRedirect(reverse("view_cart"))

	#assign address
	#run credit card
	if new_order.status == "Finished":
		del request.session["cart_id"]
		del request.session["total_items"]
		return HttpResponseRedirect(reverse("view_cart"))

	context={}
	template="products/home.html"
	return render(request,template,context)