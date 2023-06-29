# Generated by Django 4.1.7 on 2023-06-29 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_travelticketsapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelpackagesapplication',
            name='applicants_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='travelpackagesapplication',
            name='stage',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='travelpackagesapplication',
            name='status',
            field=models.CharField(default='open', max_length=200),
        ),
        migrations.AddField(
            model_name='travelticketsapplication',
            name='applicants_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='travelticketsapplication',
            name='stage',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='travelticketsapplication',
            name='status',
            field=models.CharField(default='open', max_length=200),
        ),
        migrations.AddField(
            model_name='travelvisaapplication',
            name='stage',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='travelvisaapplication',
            name='status',
            field=models.CharField(default='open', max_length=200),
        ),
        migrations.AlterField(
            model_name='travelvisaapplication',
            name='courier_in_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='travelvisaapplication',
            name='courier_out_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='travelvisaapplication',
            name='document_collection_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='travelvisaapplication',
            name='handover_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='travelvisaapplication',
            name='invoice_status',
            field=models.BooleanField(default=False),
        ),
    ]