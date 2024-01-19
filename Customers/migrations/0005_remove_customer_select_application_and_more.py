# Generated by Django 4.2.9 on 2024-01-19 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0004_alter_customer_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='select_application',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='payment_status',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
