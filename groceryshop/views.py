from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Food, Cart

# Create your views here.


def get_user_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def category_selection(request):
    categories = Category.objects.all()
    return render(request, 'groceryshop/category_selection.html', {'categories': categories})


def category_food_items(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    food_items = Food.objects.filter(category=category)
    return render(request, 'groceryshop/category_food_items.html', {'category': category, 'food_items': food_items})


def add_to_cart(request, food_name):
    food_item = get_object_or_404(Food, name=food_name)
    user_cart = get_user_cart(request)
    user_cart[food_item.name] = user_cart.get(food_item.name, 0) + 1

    request.session.modified = True   # Mark the session as modified to save changes
    return redirect('category_food_items', category_name=food_item.category.name)


def remove_from_cart(request, food_name):
    food_item = get_object_or_404(Food, name=food_name)
    user_cart = get_user_cart(request)

    if food_item.name in user_cart:
        del user_cart[food_item.name]
        request.session.modified = True  # Save changes to the session

    return redirect('view_cart')  # Redirect to the cart view after removal
