# Generated by Django 4.2.6 on 2023-11-13 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(editable=False, max_length=15),
        ),
    ]
