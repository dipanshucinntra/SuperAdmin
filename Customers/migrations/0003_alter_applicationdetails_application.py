# Generated by Django 4.2.9 on 2024-01-19 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Applications', '0001_initial'),
        ('Customers', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationdetails',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Applications.application'),
        ),
    ]