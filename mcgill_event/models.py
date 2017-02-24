from django.db import models

# Create your models here.

class McGillEvent(models.Model):
    event_name = models.CharField(max_length=70)
    event_date = models.DateTimeField()
    event_link = models.URLField()