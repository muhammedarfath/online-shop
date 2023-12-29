# Generated by Django 4.2.6 on 2023-11-16 11:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0003_coupon_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiration_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]