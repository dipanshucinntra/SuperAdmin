from django.db import models

# Create your models here.
class Application(models.Model):
    application_name =  models.CharField(max_length=100, blank=True)
    about_application =  models.CharField(max_length=1000, blank=True)
    create_at =  models.DateTimeField(auto_now_add = True)
    update_at =  models.DateTimeField(auto_now_add = True)

    def __str__(self):        
        return self.application_name