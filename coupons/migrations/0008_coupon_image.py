# Generated by Django 4.2.6 on 2023-11-28 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0007_coupon_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/'),
        ),
    ]
