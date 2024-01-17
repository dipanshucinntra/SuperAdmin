from django.db import models
from datetime import datetime, date
from pytz import timezone

now = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
currentDate = date.today()
currentTime = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S')

# Create your models here.
class PyamentsHistory(models.Model):
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    invoice_number = models.CharField(max_length=30, blank=True, null=True)
    transaction_mode = models.CharField(max_length=50, blank=True, null=True)
    total_amount = models.CharField(max_length=30, blank=True, null=True)
    received_amount = models.CharField(max_length=30, blank=True, null=True)
    due_amount = models.CharField(max_length=30, blank=True, null=True)
    payment_date = models.CharField(max_length=50, blank=True, null=True)
    due_date = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=1000, blank=True, null=True)


class Attachment(models.Model):
	file_url = models.CharField(max_length=150, blank=True)
	link_type = models.CharField(max_length=100, blank=True)
	caption = models.CharField(max_length=500, blank=True) # Caption or Remark 
	link_id = models.IntegerField(default=0)
	create_date = models.CharField(default=currentDate, max_length=100, blank=True)
	create_time = models.CharField(default=currentTime, max_length=100, blank=True)
	update_date = models.CharField(default=currentDate, max_length=100, blank=True)
	update_time = models.CharField(default=currentTime, max_length=100, blank=True)
	size = models.CharField(max_length=100, blank=True) #added by millan on 10-November-2022 for storing size of attachment