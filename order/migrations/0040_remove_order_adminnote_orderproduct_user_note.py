# Generated by Django 4.2.6 on 2023-12-06 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0039_rename_user_status_order_user_product_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='adminnote',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='user_note',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
