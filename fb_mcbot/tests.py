from django.test import TestCase
from fb_mcbot.models import FBUser
from fb_mcbot import views
# Create your tests here.

class FBUserTestCase(TestCase):
    def setUp(self):
        FBUser.objects.create(first_name = "Thomas", last_name = "Oo")
    def testName(self):
        user = FBUser.objects.get(first_name = "Thomas")
        self.assertEqual(str(user), 'Thomas Oo')
    def testPersistance(self):
        b = FBUser(first_name = "Lawrence", last_name = "Tun")
        b.save()

        c = FBUser.objects.get(id = b.pk)
        self.assertEquals(c,b)

class ViewsTestCase(TestCase):
    def testCheckForUser(self):
        user_id = 1000000000000000
        existance = views.userExists(user_id)
        self.assertEquals(existance, False)