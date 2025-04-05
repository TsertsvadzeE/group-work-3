from django import forms
from .models import Dish, Order, Review


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', "category", 'description', 'price', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
