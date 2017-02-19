from django.test import TestCase
from bot_services import user_service

class ViewsTestCase(TestCase):
    def testCheckForUser(self):
        user_id = 1000000000000000
        existance = user_service.userExists(user_id)
        self.assertEquals(existance, False)