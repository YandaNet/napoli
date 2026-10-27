from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish
from .forms import DishForm
from django.contrib import messages
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
            # Тут у реальному проєкті можна зберігати замовлення в БД або відправляти в Telegram
            data = form.cleaned_data
            messages.success(request, f"Дякуємо, {data['full_name']}! Ваше замовлення прийнято й готується до відправки.")
            return redirect('menu:home')
    else:
        form = DeliveryForm()

    return render(request, 'menu/delivery.html', {'form': form})