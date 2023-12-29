# Generated by Django 4.2.6 on 2023-11-12 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
        ('order', '0006_shopcart_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='coupons',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupons.coupon'),
        ),
    ]