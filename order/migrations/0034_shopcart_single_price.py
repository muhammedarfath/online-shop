# Generated by Django 4.2.6 on 2023-11-29 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0033_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='single_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]