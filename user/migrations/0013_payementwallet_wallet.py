# Generated by Django 4.2.6 on 2023-12-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_userprofile_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='payementwallet',
            name='wallet',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]