# Generated by Django 4.2.6 on 2023-11-17 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_variants_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variants',
            name='slug',
        ),
    ]
