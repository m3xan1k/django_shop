# Generated by Django 2.1.7 on 2019-03-01 14:06

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20190301_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='meta_keywords',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_keywords',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
