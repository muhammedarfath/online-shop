# Generated by Django 4.2.6 on 2023-11-16 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0005_alter_coupon_expiration_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='one_time_use',
            field=models.BooleanField(default=False),
        ),
    ]
