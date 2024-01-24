# Generated by Django 4.2.3 on 2023-11-04 21:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopswift', '0006_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_product_size',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopswift.customer'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateField(default=datetime.datetime.today, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopswift.product'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_product_quantity',
            field=models.IntegerField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_product_rate',
            field=models.IntegerField(null=True),
        ),
    ]