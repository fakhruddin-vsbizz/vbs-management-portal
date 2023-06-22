# Generated by Django 4.1.7 on 2023-06-22 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel', '0002_travelclient'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelclient',
            name='admin_auth_user_ref',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]