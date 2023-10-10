from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Food)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    saved_carts = models.ManyToManyField('SavedCart', blank=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def add_item(self, food_item):
        self.items.add(food_item)

    def remove_item(self, food_item):
        self.items.remove(food_item)

    def get_total_price(self):
        total_price = 0
        for food_item in self.items.all():
            total_price += food_item.price
        return total_price

    def clear(self):
        self.items.clear()

    def get_item_count(self):
        return self.items.count()
    
    def save_cart_for_later(self, name):
        saved_cart = SavedCart(user=self.user, name=name)
        saved_cart.save()
        saved_cart.items.set(self.items.all())
        self.saved_carts.add(saved_cart)
        self.clear()

    def delete_cart(self):
        self.delete()

class SavedCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    items = models.ManyToManyField('Food')
    created_at = models.DateTimeField(timezone.now)

    def __str__(self):
        return self.name

    def delete_saved_cart(self):
        self.delete()
        