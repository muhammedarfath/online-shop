# Generated by Django 4.2.6 on 2023-11-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='offer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
