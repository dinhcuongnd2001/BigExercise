# Generated by Django 3.2.8 on 2021-11-30 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_customer_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
