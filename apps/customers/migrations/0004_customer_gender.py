# Generated by Django 5.0.5 on 2024-06-06 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')], max_length=1, null=True),
        ),
    ]
