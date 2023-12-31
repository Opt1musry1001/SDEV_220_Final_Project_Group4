from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Food, SavedCart
from django.contrib.auth.decorators import login_required


# View to display a list of all categories
def category_selection(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'groceryshop/category_selection.html', {'categories': categories})

# View to display food items of a specific category
def category_food_items(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    food_items = Food.objects.filter(category=category).order_by('name')
    return render(request, 'groceryshop/category_food_items.html', {'category': category, 'food_items': food_items})

# View to get the user's shopping cart
@login_required
def get_user_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

# View to add a food item to the shopping cart
@login_required
def add_to_cart(request, food_name):
    food_item = get_object_or_404(Food, name=food_name)
    user_cart = get_user_cart(request)
    user_cart[food_item.name] = user_cart.get(food_item.name, 0) + 1

    request.session.modified = True   # Mark the session as modified to save changes
    return redirect('category_food_items', category_name=food_item.category.name)

# View to remove a food item from the shopping cart
@login_required
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

# View to display the contents of user's shopping cart
@login_required
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


# View to save the current cart for later
def save_cart_for_later(request, name):
    saved_cart = SavedCart(user=request.user, name=name)
    saved_cart.save()
    saved_cart.items.set(request.session['cart'].keys())
    request.user.cart.saved_carts.add(saved_cart)
    request.session['cart'] = {}

# View to display a list of saved carts
def saved_carts(request, saved_carts_id):
    saved_carts = get_object_or_404(SavedCart, id=saved_carts_id, user=request.user)
    return render(request, 'groceryshop/view_saved_carts.html', {'saved_carts': saved_carts})

# View to view the contents of a saved cart
def view_saved_cart(request, saved_cart_id):
    saved_cart = get_object_or_404(SavedCart, id=saved_cart_id, user=request.user)
    return render(request, 'groceryshop/view_saved_cart.html', {'saved_cart': saved_cart})

# View to remove a food item from a saved cart
def remove_from_saved_cart(request, saved_cart_id, food_name):
    saved_cart = get_object_or_404(SavedCart, id=saved_cart_id, user=request.user)
    food_item = get_object_or_404(Food, name=food_name)

    # Remove the food item from the saved cart
    saved_cart.items.remove(food_item)

    return redirect('view_saved_cart', saved_cart_id=saved_cart_id)

# View to delete a saved cart
def delete_saved_cart(request, saved_cart_id):
    saved_cart = get_object_or_404(SavedCart, id=saved_cart_id, user=request.user)
    saved_cart.delete()
    return redirect('view_cart')  # Redirect to the cart view after deletion
