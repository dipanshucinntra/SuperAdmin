# Generated by Django 4.2.9 on 2024-01-19 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Industries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_name', models.CharField(blank=True, max_length=100)),
                ('industry_code', models.CharField(blank=True, max_length=5)),
                ('industry_desc', models.CharField(blank=True, max_length=200)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
