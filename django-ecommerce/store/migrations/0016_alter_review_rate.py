# Generated by Django 3.2.8 on 2021-11-28 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5),
        ),
    ]
