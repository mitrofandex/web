# Generated by Django 2.1.5 on 2019-02-09 15:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_auto_20190208_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='likes_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
