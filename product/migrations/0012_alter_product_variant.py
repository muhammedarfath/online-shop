# Generated by Django 4.2.6 on 2023-11-16 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_product_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='variant',
            field=models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='None', max_length=30),
        ),
    ]
