from django.db import models

# Create your models here.

class InstaImage(models.Model):

    image_link = models.CharField(max_length=255, unique=True)
    post_link = models.CharField(max_length=255, unique=True)
    post_description = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']
