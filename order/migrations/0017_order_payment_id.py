# Generated by Django 4.2.6 on 2023-11-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_orderproduct_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
