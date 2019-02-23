from django import forms
from .models import *
from django.utils import timezone


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'buying_type',
            'address',
            'delivery_date',
            'comments',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'buying_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес доставки'}),
            'delivery_date': forms.SelectDateWidget(),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий к заказу'}),
        }
        labels = {
            'buying_type': 'Доставка или самовывоз?',
        }
