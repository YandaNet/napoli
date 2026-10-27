from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/add/', views.dish_create, name='dish_create'),
    path('menu/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('menu/<int:dish_id>/edit', views.dish_update, name='dish_update'),
    path('menu/<int:dish_id>/delete', views.dish_delete, name='dish_delete'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('cart/', views.cart_detail, name='cart_detail'),
path('cart/add/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
path('cart/remove/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
]