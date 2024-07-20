# Generated by Django 4.2.5 on 2024-07-19 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart_id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='')),
                ('product', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('discription', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Ec_ProductModel',
            },
        ),
        migrations.CreateModel(
            name='OrderdModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lastname', models.CharField(max_length=10)),
                ('firstname', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=255)),
                ('address1', models.CharField(max_length=50)),
                ('address2', models.CharField(max_length=50)),
                ('holder', models.CharField(max_length=20)),
                ('credit_card_number', models.BigIntegerField()),
                ('date_of_expiry', models.CharField()),
                ('security_code', models.IntegerField()),
                ('items', models.JSONField()),
                ('total_price', models.IntegerField()),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ec.cartmodel')),
            ],
            options={
                'db_table': 'Ec_OrderdModel',
            },
        ),
        migrations.CreateModel(
            name='CartItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ec.cartmodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ec.productmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
