# Generated by Django 4.2 on 2025-03-14 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='delivery',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='payments',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_items',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
