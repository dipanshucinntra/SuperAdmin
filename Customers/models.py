from django.db import models
from Applications.models import Application
from Industries.models import Industries

# Create your models here.
class Customer(models.Model):
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE, editable=True)
    customer_name = models.CharField(max_length=255)    
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
    

class Employee(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, editable=True)
    user_name = models.CharField(max_length=100, blank=False, null=False)
    phone_no = models.CharField(max_length=15, blank=False, null=False)
    email = models.CharField(max_length=70, blank=False, null=False)
    start_date = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.user_name
    

class ApplicationDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, editable=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, editable=True)
    license_cost = models.CharField(max_length=100, blank=False, null=False)
    active_users =models.CharField(max_length=100, blank=False, null=False)
    url = models.CharField(max_length=100, blank=False, null=False)
    start_date = models.CharField(max_length=100, blank=False, null=False)
    end_date = models.CharField(max_length=100, blank=False, null=False)
    payment_frequency = models.CharField(max_length=100, blank=False, null=False)
   