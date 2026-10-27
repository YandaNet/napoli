from django import forms
from .models import Dish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "description", "price", "category", "is_available"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class DeliveryForm(forms.Form):
    full_name = forms.CharField(
        label="ПІБ покупця", 
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Шевченко Тарас Григорович'})
    )
    phone = forms.CharField(
        label="Номер телефону", 
        max_length=20, 
        widget=forms.TextInput(attrs={'placeholder': '+380 XX XXX XX XX'})
    )
    address = forms.CharField(
        label="Адреса доставки", 
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'вул. Незалежності, 10, кв. 15'})
    )
    PAYMENT_CHOICES = [
        ('card_online', 'Карткою онлайн'),
        ('cash_courier', 'Готівкою кур’єру'),
        ('card_courier', 'Карткою кур’єру (термінал)'),
    ]
    payment_method = forms.ChoiceField(
        label="Спосіб оплати", 
        choices=PAYMENT_CHOICES, 
        widget=forms.Select()
    )
    comment = forms.CharField(
        label="Коментар до замовлення (необов'язково)", 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Дзвінок у двері не працює, під\'їзд №2...'})
    )