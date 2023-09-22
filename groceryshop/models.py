from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


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
    inventory = models.IntegerField
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField
    image = models.ImageField(upload_to='food_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.
                             CASCADE)
    # ?? models.OneToOneField(user, on_delete=models.CASCADE)
    items = models.ManyToManyField('Food')
    created_at = models.DateTimeField(timezone.now)  # or (auto_now_add=True)
    updated_at = models.DateTimeField(timezone.now)
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
        for item in self.items.all():
            total_price += item.price
        return total_price

    def finalize(self):
        self.is_active = False
        self.save()

    def clear(self):
        self.items.clear()

    def get_item_count(self):
        return self.items.count()

    def save_cart_for_later(self, name):
        saved_cart = SavedCart(name=name)
        saved_cart.save()
        saved_cart.items.set(self.items.all())
        self.saved_carts.add(saved_cart)


class SavedCart(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField('Food')
    created_at = models.DateTimeField(timezone.now)

    def __str__(self):
        return self.name
