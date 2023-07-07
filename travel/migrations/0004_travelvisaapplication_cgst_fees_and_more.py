# Generated by Django 4.1.7 on 2023-07-05 10:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_travelpackagesapplication_first_installment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelvisaapplication',
            name='cgst_fees',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='travelvisaapplication',
            name='sgst_fees',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='followups',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='followups',
            name='time_for_followups',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='travelapplicationcontroltransfer',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='travelclient',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='travelpackagesapplication',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='travelpackagesvendorpayment',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='travelticketsapplication',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='travelvisaapplication',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='vbsemployeedetails',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]