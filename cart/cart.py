from Store.models import Product, Profile

class Cart():
	def __init__(self, request):
		self.session = request.session
		self.request = request
		cart = self.session.get('session_key')

		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}


		self.cart = cart
    
	def add(self, product):
		product_id = str(product.id)
		product_qnt = str("1")
		# Logic
		if product_id in self.cart:
			pass
		else:
			#self.cart[product_id] = Decimal(product.price.replace(',', ''))
			self.cart[product_id] = int(product_qnt)

		self.session.modified = True
  
		if self.request.user.is_authenticated:
			current_user= Profile.objects.filter(user__id=self.request.user.id)
			cartier = str(self.cart)
			cartier = cartier.replace("\'","\"")
			current_user.update(old_cart=str(cartier))
  
	def __len__(self):
		return len(self.cart)

	def get_prods(self):
		# Get ids from cart
		product_ids = self.cart.keys()
		# Use ids to lookup products in database model
		products = Product.objects.filter(id__in=product_ids)

		# Return those looked up products
		return products

	def get_quants(self):
		quantities = self.cart
		return quantities

	def delete(self, product):
		product_id = str(product)
		# Delete from dictionary/cart
		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified = True
  
		if self.request.user.is_authenticated:
			current_user= Profile.objects.filter(user__id=self.request.user.id)
			cartier = str(self.cart)
			cartier = cartier.replace("\'","\"")
			current_user.update(old_cart=str(cartier))
  
	def cart_total(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		quantities = self.cart
		total = 0
  
		for key, value in quantities.items():
			key = int(key)
			for product in products:
				if product.id == key:
					total = total + (product.price)
     
		return total 

	def db_add(self, product):
		product_id = str(product)
		product_qnt = str("1")
		# Logic
		if product_id in self.cart:
			pass
		else:
			 #self.cart[product_id] = int(product.price.replace(',', ''))
			self.cart[product_id] = int(product_qnt)

		self.session.modified = True
  
		if self.request.user.is_authenticated:
			current_user= Profile.objects.filter(user__id=self.request.user.id)
			cartier = str(self.cart)
			cartier = cartier.replace("\'","\"")
			current_user.update(old_cart=str(cartier))       
            
            
                
                    
                    
                    
        