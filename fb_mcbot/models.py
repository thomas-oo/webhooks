from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class FBUser(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    user_id = models.SlugField(default='', max_length=16, validators=[MinLengthValidator(16)]) #contains only letters, numbers, underscores, or hyphens, usually used in URLs
    user_type = models.CharField(max_length=70, null=True)

    def __str__(self):
        return ("%s %s" % (self.first_name , self.last_name))

    def set_user_type(self, user_type):
        self.user_type = user_type
        self.save()

class Conversation(models.Model):
    fbuser = models.ForeignKey(FBUser, on_delete=models.CASCADE)
    question = models.PositiveIntegerField()

    def __str__(self):
        return ("%s %s" % (self.fbuser.first_name , self.question))

    def set_conversation_question(self, question):
        self.question = question
        self.save();
