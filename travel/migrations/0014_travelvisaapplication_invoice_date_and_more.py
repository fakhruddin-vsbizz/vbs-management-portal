# Generated by Django 4.1.7 on 2023-08-25 05:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0013_remove_travelvisaapplication_collection_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelvisaapplication',
            name='invoice_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='travelpackagesapplication',
            name='arrival_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 25, 10, 47, 51, 590082), null=True),
        ),
        migrations.AlterField(
            model_name='travelpackagesapplication',
            name='departure_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 25, 10, 47, 51, 590082), null=True),
        ),
        migrations.AlterField(
            model_name='travelpackagesapplication',
            name='tentative_payment_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 25, 10, 47, 51, 590082), null=True),
        ),
        migrations.AlterField(
            model_name='travelticketsapplication',
            name='arrival_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 25, 10, 47, 51, 590082), null=True),
        ),
        migrations.AlterField(
            model_name='travelticketsapplication',
            name='departure_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 25, 10, 47, 51, 590082), null=True),
        ),
    ]