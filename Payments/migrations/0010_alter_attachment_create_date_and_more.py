# Generated by Django 4.2.9 on 2024-01-20 16:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0009_alter_attachment_create_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='create_date',
            field=models.CharField(blank=True, default=datetime.date(2024, 1, 20), max_length=100),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='create_time',
            field=models.CharField(blank=True, default='21:30:01', max_length=100),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='update_date',
            field=models.CharField(blank=True, default=datetime.date(2024, 1, 20), max_length=100),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='update_time',
            field=models.CharField(blank=True, default='21:30:01', max_length=100),
        ),
    ]
