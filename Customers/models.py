from django.db import models
from Applications.models import Application
from Industries.models import Industries

# Create your models here.
class Customer(models.Model):
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255, blank=True)    
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    address = models.TextField()
    payment_status = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.CustomerName
    

class Employee(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, blank=False, null=False)
    phone_no = models.CharField(max_length=15, blank=False, null=False)
    email = models.CharField(max_length=70, blank=False, null=False)
    start_date = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.user_name
    

class ApplicationDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    application = models.ManyToManyField(Application) #, blank=True, null=True
    license_cost = models.CharField(max_length=100, blank=False, null=False)
    active_users =models.CharField(max_length=100, blank=False, null=False)
    url = models.CharField(max_length=100, blank=False, null=False)
    start_date = models.CharField(max_length=100, blank=False, null=False)
    end_date = models.CharField(max_length=100, blank=False, null=False)
    payment_frequency = models.CharField(max_length=100, blank=False, null=False)
   