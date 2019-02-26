from django import forms
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User


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

        help_texts = {
            'buying_type': 'Доставка или самовывоз?',
            'delivery_date': 'Время доставки согласовывается дополнительно',
            'email': 'Мы не передаем вашу почту третьим лицам'
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте логин'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}),
        }


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('Введите своё имя')
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Введите свою фамилию')
        return last_name


    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username):
            raise forms.ValidationError('Пользователь с таким логином уже зарегистрирован, придумайте другой логин')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Пользователь с почтой "{}" уже зарегистрирован, проверьте свой почтовый ящик, там есть письмо с учетными данными'.format(email))
        return email


class LoginForm(forms.Form):
    username = forms.CharField(help_text='Введите ваш логин')
    password = forms.CharField(widget=forms.PasswordInput, help_text='Введите ваш пароль')

    username.widget.attrs.update({'class': 'form-control', 'placeholder': 'Ваш логин'})
    password.widget.attrs.update({'class': 'form-control', 'placeholder': 'Ваш пароль'})

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=username):
            raise forms.ValidationError('Пользователь "{}" не зарегистрирован'.format(username))

        user = User.objects.get(username=username)
        # base_password = User.objects.get(username=username).password

        if user and not user.check_password(password):
            raise forms.ValidationError('Неправильный пароль')
        return self.cleaned_data
