# Generated by Django 5.0.5 on 2024-05-28 16:49

import apps.products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.products.models.brand_image_upload_to),
        ),
    ]
