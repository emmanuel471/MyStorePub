from email.message import EmailMessage
import json
from .models import Product, Testimonial, Video, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, TestimonialForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ProfilePic
from cart.cart import Cart
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from twilio.rest import Client
import random
from django.http import HttpResponse, JsonResponse
from .mixins import MessageHandler
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render, redirect


def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Testimony Successfully Submitted")
            return redirect('home')  # Redirect to a thank you page or any other page
    else:
        form = TestimonialForm()
    return render(request, 'submit_testimonial.html', {'form': form})

def testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'testimonials.html', {'testimonials': testimonials})

def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user=request.user)
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ObjectDoesNotExist:
            messages.error(request, "We are still reviewing you account, try again in few 30 min.Thank you for understanding")
            return redirect('home')  
        
        form = UserInfoForm(request.POST or None, request.FILES or None , instance=current_user)		
        
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated!!")
            return redirect('home')
        
        return render(request, "update_info.html", {'form': form})
    else:
        messages.error(request, "You are not authenticated!!")
        return redirect('home')  
                        
def home(request):
    
    video = Video.objects.all()
    products = Product.objects.all()
    searched = 'Quick navigation'
    
    if request.method == "POST":
        searcheditm = request.POST['searched']
        return render(request, 'index.html',{'products': products,'video':video,'searched': searcheditm})
    else:
        return render(request, 'index.html',{'products': products,'video':video,'searched': searched})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    
    if request.method =="POST":

        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                
                for key,value in converted_cart.items():
                    cart.db_add(product=key)
            
            messages.success(request,("successfully logged in"))
            return redirect('home')
        
        else:
            messages.success(request,("Invalid credentials!!"))
            return redirect('login')
    else:       
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("Successfully Logged out!!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)  
        
        if form.is_valid():
            # Process form data
            
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['first_name']
            
            # Prepare email content
            subject = 'Welcome to GearFarmEssentials'
            message = f'''
            Hi {firstname},

            Welcome to GearFarmEssentials!

            We are thrilled to have you on board and look forward to supporting you in optimizing your gear farming experience. Our platform offers a comprehensive set of tools and resources tailored to meet your farming needs, whether you're cultivating crops, raising livestock, or managing agricultural projects.

            From advanced analytics to expert guidance, GearFarmEssentials is here to empower you every step of the way. Dive into our features, connect with fellow farmers, and unlock the full potential of your farming endeavors. Let's grow together and cultivate success in the world of agriculture!

            Best regards,
            The GearFarmEssentials Team
            '''

            # Create an EmailMessage instance
            email_message = EmailMessage()
            email_message.subject = subject
            email_message.body = message
            email_message.from_email = settings.EMAIL_HOST_USER
            email_message.to = [email]

            # Attach the PDF file
            pdf_file_path = 'media/uploads/product/GearFarmEssentials.pdf'  # Update with the actual file path
            with open(pdf_file_path, 'rb') as pdf_file:
                email_message.attach('ourstore.pdf', pdf_file.read(), 'application/pdf')

            # Send the email
            email_message.send(fail_silently=False)

            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
        else:
            messages.error(request, "Oops! Something went wrong. Please try again.")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
  
def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})   
    

def update_user(request):
    
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)  
        profile_user = Profile.objects.get(user__id=request.user.id)
        
        form = UpdateUserForm(request.POST or None, request.FILES or None,instance=current_user) 
        pic_form = ProfilePic(request.POST or None, request.FILES or None,instance=profile_user) 
        
        if form.is_valid() and pic_form.is_valid():        
            form.save()
            pic_form.save()
            login(request, current_user)
            messages.success(request, "Successfully updated!!")
            return redirect('home')
        return render(request, 'update_user.html',{'form':form, 'pc_form': pic_form})
                        
    else: 
        messages.success(request, "You are not authenticated")
        return redirect('home')
        
def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')


def user_profile(request):

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile
    }
    return render(request, 'user_profile.html', context)

        
def message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('message') 
        our_email = settings.EMAIL_HOST_USER
        
        send_mail(
            f'Message from {name}',
            f'Name: {name}\n\nEmail: {email}\n\nNumber: {number}\n\nMessage: {message}',
            email,
            [our_email],
            fail_silently=False,
        )
        
        messages.success(request,'Message sent successfully!')
    return render(request, 'message.html')        
