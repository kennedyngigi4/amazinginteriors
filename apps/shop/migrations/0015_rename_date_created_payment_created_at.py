# Generated by Django 4.2 on 2025-03-15 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='date_created',
            new_name='created_at',
        ),
    ]
