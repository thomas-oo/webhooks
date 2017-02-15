from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot_email.emailbot import Email

import requests

import facebook

from json import dumps, loads
from pprint import pprint


APP_ID = '362191170829320'
APP_SECRET = 'b89bdf1697d83f88c606bbffbc8487bb'
VERIFY_TOKEN = '2318934571'
# Permanent page access token
PAGE_ACCESS_TOKEN = 'EAAFJaTQTZCAgBAKquTNCRxUz2edEmSuocZC9EreThZAiGFImZAHGGqVlcLdvRDe3vMNXZBvXnQL3ZC0VMJY8IMAWt6t0j8tZCBwsYBZAQDEYOh1kwdjzmnu6zkg1tPyWITWTtgcQvZAw0mvyqZAIkZABmmkMQr1UQwBCkKkcXCTmaZAFHAZDZD'

TEMP_EMAIL_ADDRESS = 'mcbot.ecse428@gmail.com'
TEMP_EMAIL_PASSWORD = 'mcbotmcbot428'

def post_facebook_message(fbid, received_message):
    # TODO Change access token
    post_message_url = 'https://graph.facebook.com/v2.8/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    response_msg = dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print('SEND STATUS')
    pprint(status.json())
    email = Email(TEMP_EMAIL_ADDRESS, TEMP_EMAIL_PASSWORD, received_message, 'email from bot')
    email.send_email()

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
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
