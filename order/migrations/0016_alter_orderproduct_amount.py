# Generated by Django 4.2.6 on 2023-11-13 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_alter_orderproduct_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='amount',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
