# Generated by Django 4.2.5 on 2024-07-16 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0006_rename_name_productmodel_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartmodel',
            old_name='cart',
            new_name='cart_id',
        ),
    ]