from django.db import models

# Create your models here.
class Industries(models.Model):    
    industry_name = models.CharField(max_length=100, blank=True)
    industry_code = models.CharField(max_length=5, blank=True)
    industry_desc = models.CharField(max_length=200, blank=True)
    create_at =  models.DateTimeField(auto_now_add = True)
    update_at =  models.DateTimeField(auto_now_add = True)
