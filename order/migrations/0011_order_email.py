# Generated by Django 4.2.6 on 2023-11-13 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_rename_country_order_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]