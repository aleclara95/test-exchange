# Generated by Django 3.1.3 on 2020-11-21 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_order_original_amount'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='currencypair',
            unique_together={('origin', 'destination')},
        ),
    ]
