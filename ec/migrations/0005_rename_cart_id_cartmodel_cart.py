# Generated by Django 4.2.5 on 2024-07-16 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0004_rename_cart_id_cartitemmodel_cart_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartmodel',
            old_name='cart_id',
            new_name='cart',
        ),
    ]
