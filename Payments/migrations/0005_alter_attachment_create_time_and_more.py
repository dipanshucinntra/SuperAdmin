# Generated by Django 4.2.9 on 2024-01-19 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0004_alter_attachment_create_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='create_time',
            field=models.CharField(blank=True, default='12:17:36', max_length=100),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='update_time',
            field=models.CharField(blank=True, default='12:17:36', max_length=100),
        ),
    ]
