from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fb_mcbot.models import FBUser
from bot_email.emailbot import Email

import requests

import facebook

from json import dumps, loads
from pprint import pprint


APP_ID = '362191170829320'
APP_SECRET = 'b89bdf1697d83f88c606bbffbc8487bb'
VERIFY_TOKEN = '2318934571'
# Permanent page access token
# TODO change access token to production one before pushing.
PAGE_ACCESS_TOKEN = 'EAAFJaTQTZCAgBAKquTNCRxUz2edEmSuocZC9EreThZAiGFImZAHGGqVlcLdvRDe3vMNXZBvXnQL3ZC0VMJY8IMAWt6t0j8tZCBwsYBZAQDEYOh1kwdjzmnu6zkg1tPyWITWTtgcQvZAw0mvyqZAIkZABmmkMQr1UQwBCkKkcXCTmaZAFHAZDZD'
#PAGE_ACCESS_TOKEN = 'EAAfmEq7c1t8BAKWagwktkLR6VkFsPANAzTiykeWrjtfZAVMhJSvkbC8Mv9qh3nddrAIgoZBipWFYXw4Ahgbl2lrdagDBz7rgHIYVMDalUNkhAFQYrMPjZB9tlAB3h7N2uMQ7MIuVl4XOZASN8kmTy9Lu3KpC6VnFzTn8aWLs6wZDZD'

graph = facebook.GraphAPI(PAGE_ACCESS_TOKEN, version='2.2')
def post_facebook_message(fbid, received_message):
    # TODO Change access token
    post_message_url = 'https://graph.facebook.com/v2.8/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    response_msg = dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print('SEND STATUS')
    pprint(status.json())
    email = Email(received_message, 'email from bot')
    email.send_confirmation_email('CONFIRMATION-CODE-AABB123')

def get_user_info(user_id):
    user = requests.get(("https://graph.facebook.com/v2.6/%s?access_token=%s" % (user_id, PAGE_ACCESS_TOKEN)))
    return user

def userExists(userid):
    try:
        user = FBUser.objects.get(user_id = userid)
    except FBUser.DoesNotExist:
        pprint("User id not found in db, the user does not exist.")
        return False;
    return True;

def create_new_user(user,user_id):
    pprint("Creating new user")
    firstname = user['first_name']
    lastname = user['last_name']
    new_user = FBUser(first_name = firstname, last_name = lastname, user_id =  user_id)
    new_user.save()

# Create your views here.
class McBotView(generic.View):
    def get(self, request, *args, **kwargs):
        # TODO Change the verify_token
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = loads(self.request.body.decode('utf-8'))
        print('INCOMING MESSAGE')
        pprint(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    #pprint(message)
                    user_id = (message['sender']['id'])
                    user = get_user_info(user_id).json()
                    if(userExists(user_id) == False):
                        create_new_user(user,user_id)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

