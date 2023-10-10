from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_selection, name='category_selection'),
    path('category/<str:category_name>/', views.category_food_items, name='category_food_items'),
    path('add_to_cart/<str:food_name>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:food_name>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('save_cart_for_later/', views.save_cart_for_later, name='save_cart_for_later'),
    path('view_saved_cart/<int:saved_cart_id>/', views.view_saved_cart, name='view_saved_cart'),
    path('delete_saved_cart/<int:saved_cart_id>/', views.delete_saved_cart, name='delete_saved_cart'),
    path('remove_from_saved_cart/<int:saved_cart_id>/<str:food_name>/', views.remove_from_saved_cart, name='remove_from_saved_cart'),
]
