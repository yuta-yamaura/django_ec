# Generated by Django 4.2.5 on 2024-07-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdmodel',
            name='total_price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]