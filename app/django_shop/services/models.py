from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from transliterate import translit
from time import time
from django.urls import reverse

# Create your models here.

def gen_slug(title):
    try:
        new_slug = slugify(translit(title, reversed=True), allow_unicode=True)
    except Exception as e:
        print(e)
        new_slug = slugify(title, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

def image_folder(instance, filename):
    file_ext = filename.split('.')[1]
    filename = '{}.{}'.format(instance.slug, file_ext)
    return '{}/{}'.format(instance.slug, filename)


class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    body = RichTextUploadingField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail_url', kwargs={'slug': self.slug})
