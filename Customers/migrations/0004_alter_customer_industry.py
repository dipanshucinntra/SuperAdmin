# Generated by Django 4.2.9 on 2024-01-19 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Industries', '0001_initial'),
        ('Customers', '0003_alter_applicationdetails_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Industries.industries'),
        ),
    ]
