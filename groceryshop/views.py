from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Food, Cart

# Create your views here.


def category_selection(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'groceryshop/category_selection.html', {'categories': categories})


def category_food_items(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    food_items = Food.objects.filter(category=category).order_by('name')
    return render(request, 'groceryshop/category_food_items.html', {'category': category, 'food_items': food_items})


def get_user_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


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
        if user_cart[food_item.name] > 1:
            user_cart[food_item.name] -= 1
        else:
            del user_cart[food_item.name]
            
        request.session.modified = True  # Save changes to the session

    return redirect('view_cart')  # Redirect to the cart view after removal


def view_cart(request):
    user_cart = get_user_cart(request)
    food_item_names = user_cart.keys()

    food_items = Food.objects.filter(name__in=food_item_names)
    
    item_prices = [(food_item.name, food_item.price) for food_item in food_items]
    

    total_price = sum(price * user_cart[food_name] for food_name, price in item_prices)
    
    context = {
        'cart': user_cart,
        'food_items': food_items,
        'item_prices': item_prices,
        'total_price': total_price,
    }

    return render(request, 'groceryshop/cart.html', context)
