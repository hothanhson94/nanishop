# Generated by Django 5.0.5 on 2024-05-28 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=100, null=True),
        ),
    ]