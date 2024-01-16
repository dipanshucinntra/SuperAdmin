from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    select_application = models.CharField(max_length=255)
    url = models.URLField()
    active_users = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_status = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=255)

def __str__(self):
    return self.CustomerName
