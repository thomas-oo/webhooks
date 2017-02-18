from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class FBUser(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    user_id = models.SlugField(default='', max_length=16, validators=[MinLengthValidator(16)]) #contains only letters, numbers, underscores, or hyphens, usually used in URLs

    def __str__(self):
        return ("%s %s" % (self.first_name , self.last_name))
