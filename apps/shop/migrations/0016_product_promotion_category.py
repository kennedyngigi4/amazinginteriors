# Generated by Django 4.2 on 2025-03-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_rename_date_created_payment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='promotion_category',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
