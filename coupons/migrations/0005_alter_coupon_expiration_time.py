# Generated by Django 4.2.6 on 2023-11-16 11:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0004_alter_coupon_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiration_time',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
    ]