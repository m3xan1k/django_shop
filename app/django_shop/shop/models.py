from __future__ import unicode_literals

from django.db import models
from time import time
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import random

# Create your models here.

def gen_slug(title):
    try:
        new_slug = slugify(translit(title, reversed=True), allow_unicode=True)
    except:
        new_slug = slugify(title, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']


class Brand(models.Model):
    title = models.CharField(max_length=100)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    def __str__(self):
        return self.title


def image_folder(instance, filename):
    file_ext = filename.split('.')[1]
    filename = '{}.{}'.format(instance.slug, file_ext)
    return '{}/{}'.format(instance.slug, filename)


class ProductManager(models.Manager):
    def get_random_three(self):
        return [random.choice(self.all()) for x in range(3)]



class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)

    class Meta:
        ordering = ['-price']


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'slug': self.slug})

    objects = ProductManager()


class SliderImage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    image = models.ImageField(upload_to=image_folder)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)


class CartItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return 'Cart item for product {}'.format(self.product.title)

class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, request, slug):
        cart = self
        product = Product.objects.get(slug__iexact=slug)
        new_item = CartItem.objects.get_or_create(product=product, item_total=product.price)[0]
        if new_item not in cart.items.all():
            # так как метод .get_or_create возвращает кортеж, а объект CartItem там идет под нулевым индексом, именно его нам надо получить. Можно сделать двойное присваивание new_item, _ = ... , или можно забрать [0] от кортежа или от new_item
            cart.items.add(new_item)
            cart.save()

    # пересчет общей суммы в корзине
    def recount_cart(self):
        cart = self
        for item in cart.items.all():
            cart.cart_total += item.item_total
        return cart



ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
    ('Отгружен', 'Отгружен')
)

ORDER_BUYING_TYPE = (
    ('Самовывоз', 'Самовывоз'),
    ('Доставка', 'Доставка')
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, null=True)
    address = models.CharField(max_length=255, blank=True)
    buying_type = models.CharField(max_length=40, choices=ORDER_BUYING_TYPE, default='Доставка')
    date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=timezone.now)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return 'Заказ №{}'.format(self.id)

    def details(self):
        for item in self.items.items.all():
            print(item.product.title, item.qty)

# # making view for orders
# class OrderDetail(Order):
#     # enable proxy extends functionality withou creating table in database
#     proxy = True
#     verbose_name = 'Детали заказа'
#     verbose_name_plural = 'Детали заказа'
