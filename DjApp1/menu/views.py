from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dish
from .forms import DishForm, DeliveryForm

# Create your views here.

def home(request):
    return render(request, "menu/home.html")


def menu_list(request):
    dishes = Dish.objects.filter(is_available=True).select_related("category")
    return render(request, "menu/menu_list.html", {"dishes": dishes})


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, "menu/dish_detail.html", {"dish": dish})

def cart_detail(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'menu/cart.html', {'cart': cart, 'total_price': total_price})


def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    
    if dish_id_str in cart:
        cart[dish_id_str]['quantity'] += 1
    else:
        cart[dish_id_str] = {
            'name': dish.name,
            'price': float(dish.price),
            'quantity': 1
        }
    
    request.session['cart'] = cart
    messages.success(request, f"Страву «{dish.name}» додано до кошика!")
    return redirect('menu:menu_list')


def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    if dish_id_str in cart:
        del cart[dish_id_str]
        request.session['cart'] = cart
        messages.success(request, "Страву видалено з кошика.")
    return redirect('menu:cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    
    if request.method == 'POST':
        if not cart:
            messages.warning(request, "Ваш кошик порожній!")
            return redirect('menu:cart_detail')
            
        form = DeliveryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            if 'cart' in request.session:
                del request.session['cart']
            request.session.modified = True
            
            messages.success(request, f"Дякуємо, {data['full_name']}! Ваше замовлення успішно оформлено.")
            return redirect('menu:home')
    else:
        form = DeliveryForm()

    return render(request, 'menu/cart.html', {
        'cart': cart, 
        'total_price': total_price, 
        'form': form
    })
@login_required
def dish_create(request):
    if request.method == "POST":
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save()
            messages.success(request, "Dish created successfully")
            return redirect("menu:dish_detail", dish_id=dish.id)
    else:
        form = DishForm()
    return render(request, "menu/dish_form.html", {"form": form, "title": "Нова страва"})


@login_required
def dish_update(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == "POST":
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            messages.success(request, "Dish updated successfully")
            return redirect("menu:dish_detail", dish_id=dish.id)
    else:
        form = DishForm(instance=dish)
    return render(request, "menu/dish_form.html", {"form": form, "title": f"Редагування: {dish.name}"})


@login_required
def dish_delete(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == "POST":
        dish.delete()
        messages.success(request, "Dish deleted successfully")
        return redirect("menu:menu_list")
    return render(request, "menu/dish_confirm.html", {"dish": dish})


def delivery_view(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            messages.success(request, f"Дякуємо, {data['full_name']}! Ваше замовлення прийнято й готується до відправки.")
            return redirect('menu:home')
    else:
        form = DeliveryForm()

    return render(request, 'menu/delivery.html', {'form': form})