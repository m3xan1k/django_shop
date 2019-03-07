from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from transliterate import translit
from time import time
from django.urls import reverse

# Create your models here.

def gen_slug(title):
    try:
        new_slug = slugify(translit(title, reversed=True), allow_unicode=True)
    except:
        new_slug = slugify(title, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


def image_folder(instance, filename):
    file_ext = filename.split('.')[1]
    filename = f'{instance.slug}.{file_ext}'
    return '{}/{}'.format(instance.slug, filename)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_list_url', kwargs={'slug': self.slug})


class PostManager(models.Manager):
    def get_latest_posts(self):
        return self.all().reverse()[:2]


class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = RichTextUploadingField()
    tags = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    image = models.ImageField(upload_to=image_folder, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['pub_date']

    objects = PostManager()
