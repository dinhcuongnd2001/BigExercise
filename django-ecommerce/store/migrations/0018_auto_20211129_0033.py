# Generated by Django 3.2.8 on 2021-11-28 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0017_auto_20211129_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]