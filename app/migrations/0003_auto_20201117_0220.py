# Generated by Django 3.1.3 on 2020-11-17 02:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201117_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_create',
            field=models.DateField(default=datetime.datetime(2020, 11, 17, 2, 20, 14, 969302, tzinfo=utc)),
        ),
    ]