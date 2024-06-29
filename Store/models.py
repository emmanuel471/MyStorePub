from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.content[:50]}"
    
def get_default_image():
    return '/media/profiledefault.png'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)   
    userimage = models.ImageField(blank=True, null=True, default=get_default_image)

    def __str__(self):
	    return self.user.username

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)

class Category(models.Model):
      name = models.CharField(max_length=50)
      
      def __str__(self):
          return self.name
         
class Customer(models.Model):
      firstname = models.CharField(max_length=50)
      lastname = models.CharField(max_length=50)
      phone = models.CharField(max_length=15)
      email = models.EmailField(max_length=100)
      password = models.CharField(max_length=50)
      
      def __str__(self):
          return f'{self.firstname} {self.lastname}' 
          
class Product(models.Model):
      name =models.CharField(max_length=100)
      price = models.DecimalField(default =0, decimal_places=2,max_digits = 15)
      category = models.ForeignKey(Category, on_delete=models.CASCADE, default =1)
      description = models.CharField(max_length=250, default='', blank=True)
      image = models.ImageField(upload_to='uploads/product/')
      
      def __str__(self):
        return self.name
      
class Oder(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    quantity = models.IntegerField(default = 1, )
    address = models.CharField(max_length=100, default='',blank=True)
    phone = models.CharField(max_length=15, default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.product    
    
class Video(models.Model):
    caption = models.CharField(max_length=100)   
    video = models.FileField(upload_to="Store/%y")
    
    def __str__(self):
        return self.caption