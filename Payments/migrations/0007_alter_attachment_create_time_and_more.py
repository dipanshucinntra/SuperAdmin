# Generated by Django 4.2.9 on 2024-01-19 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0006_alter_attachment_create_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='create_time',
            field=models.CharField(blank=True, default='13:14:12', max_length=100),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='update_time',
            field=models.CharField(blank=True, default='13:14:12', max_length=100),
        ),
    ]
