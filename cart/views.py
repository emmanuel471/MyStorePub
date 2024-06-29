from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from Store.models import Product
from django.http import JsonResponse

def cart_summary(request):
	cart = Cart(request)
	cart_products = cart.get_prods
	#quantities = cart.get_quants
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products, "totals":totals})

def cart_add(request):
    
	cart = Cart(request)
	
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('product_id'))

		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
 
		cart.add(product=product)
		response = JsonResponse({'Product Name: ': product.name})
		return response
    
def cart_delete(request): 
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('product_id'))
		cart.delete(product=product_id)
		response = JsonResponse({'product':product_id})
		return response

def cart_update(request):
    pass




