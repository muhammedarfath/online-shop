# Generated by Django 4.2.6 on 2023-12-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0040_remove_order_adminnote_orderproduct_user_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'New'), (2, 'Accepted'), (3, 'Preparing'), (4, 'OnShipping'), (5, 'Completed'), (6, 'Canceled'), (7, 'Return')], default=1, null=True),
        ),
    ]
