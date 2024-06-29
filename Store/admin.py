from django.contrib import admin
from .models import Category, Customer, Product, Oder, Profile, Video, Testimonial
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Oder)
admin.site.register(Profile)
admin.site.register(Video)
admin.site.register(Testimonial)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'content')

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)