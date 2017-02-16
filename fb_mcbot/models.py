from django.db import models

# Create your models here.
class FBUser(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    timezone = models.DateField()

    def __str__(self):
        return ("%s %s" % (self.first_name , self.last_name))
