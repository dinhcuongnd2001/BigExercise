# Generated by Django 3.2.8 on 2021-11-29 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20211129_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(),
        ),
    ]