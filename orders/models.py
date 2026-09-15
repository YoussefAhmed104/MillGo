from django.db import models

# Create your models here.

class Order(models.Model):
  SERVICE_CHOICES = [
    ('SELF','I will come'),
    ('DELIVERY','delivery'),
  ]
  STATUS_CHOICES = [
    ('WAITING', 'waiting'),
    ('PROCESSING', 'processing'),
    ('COMPLETED', 'completed'),
  ]
  customer_name = models.CharField(max_length= 100)
  phone_num = models.CharField(max_length=12)
  wheat_weight_kg = models.FloatField()
  service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES, default='SELF')
  manual_location = models.TextField()

  # auto location 
  latitude = models.FloatField(null=True, blank=True)
  longtitude = models.FloatField(null=True, blank=True)

  # bill
  grinding_cost = models.FloatField(default=0.0)
  delivery_cost = models.FloatField(default=0.0)
  total_cost = models.FloatField(default=0.0)
  estimated_wait_time_minutes = models.IntegerField(default=0)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"oreder #{self.id} - {self.customer_name}"