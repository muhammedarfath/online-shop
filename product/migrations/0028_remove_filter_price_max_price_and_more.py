# Generated by Django 4.2.6 on 2023-12-26 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_filter_price_product_filter_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filter_price',
            name='max_price',
        ),
        migrations.RemoveField(
            model_name='filter_price',
            name='min_price',
        ),
        migrations.AddField(
            model_name='filter_price',
            name='price',
            field=models.CharField(choices=[('1000 TO 10000', '1000 TO 10000'), ('1000 TO 20000', '1000 TO 20000'), ('20000 TO 30000', '20000 TO 30000'), ('30000 TO 40000', '30000 TO 40000'), ('40000 TO 50000', '40000 TO 50000')], default=True, max_length=60),
            preserve_default=False,
        ),
    ]
