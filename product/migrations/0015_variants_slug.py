# Generated by Django 4.2.6 on 2023-11-17 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='variants',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
