# Generated by Django 4.2.9 on 2024-01-19 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0003_alter_applicationdetails_application'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Application',
        ),
    ]
