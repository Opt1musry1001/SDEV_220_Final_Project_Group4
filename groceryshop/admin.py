from django.contrib import admin
from .models import Food, Category, Cart, SavedCart

# Registered models.

admin.site.register(Food)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(SavedCart)
