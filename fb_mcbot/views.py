from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot_services.answer_service import AnswerService
from bot_services.communication_service import CommunicationService

import requests

from json import dumps, loads
from pprint import pprint


APP_ID = '362191170829320'
APP_SECRET = 'b89bdf1697d83f88c606bbffbc8487bb'
VERIFY_TOKEN = '2318934571'

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
                    answer = AnswerService.process_message(message)
                    CommunicationService.post_facebook_message(message['sender']['id'], answer)
        return HttpResponse()
