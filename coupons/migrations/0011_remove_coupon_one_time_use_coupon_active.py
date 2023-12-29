# Generated by Django 4.2.6 on 2023-12-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0010_alter_coupon_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='one_time_use',
        ),
        migrations.AddField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]