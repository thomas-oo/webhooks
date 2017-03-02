from django.db import models

# Create your models here.

class McgillEvent(models.Model):
    event_name = models.CharField(max_length=70)
    event_date = models.DateTimeField()
    event_link = models.URLField(blank=True)

    def __str__(self):
        return ("%s" % (self.event_name))

    def set_event_name(self, event_name):
        self.event_name = event_name
        self.save()

    def set_event_date(self, event_date):
        self.event_date = event_date
        self.save()

    def set_event_link(self, event_link):
        self.event_link = event_link
        self.save()