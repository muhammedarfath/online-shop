# Generated by Django 4.2.6 on 2023-12-18 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0042_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='grand_total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
