from __future__ import unicode_literals

from django.db import models
from time import time
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse

# Create your models here.

def gen_slug(title):
    try:
        new_slug = slugify(translit(title, reversed=True), allow_unicode=True)
    except:
        new_slug = slugify(title, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})


class Brand(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title


def image_folder(instance, filename):
    file_ext = filename.split('.')[1]
    filename = f'{instance.slug}.{file_ext}'
    return '{}/{}'.format(instance.slug, filename)


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'slug': self.slug})

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

    def __str__(self):
        return str(self.id)
