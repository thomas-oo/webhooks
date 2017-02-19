from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot_email.emailbot import Email
from bot_services.user_service import UserService, Question
from bot_services.answer_service import AnswerService

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
#PAGE_ACCESS_TOKEN = 'EAAfmEq7c1t8BAFhc9oSySXS0PvxgEZCMJulU9DnaA58jPVGD29PZCm9xsW8plpcs8xqNscA2iLpygw6L4YrwfONRracLRjkMRKMvKwWCrc7hiYIdSoyPYLMLh6CqM4ToYXQrradHbxv53WwIjl6V0ZBuKdpPBSiOKg3Ss4GcAZDZD'

MSG_ASK_FOR_USER_TYPE = 'Are you a [student] or [instructor]?'
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

    #business logic
def logic(request, message):
    user_id = (message['sender']['id'])
    pprint(user_id)
    user_info = get_user_info(user_id).json()
    fbuser = UserService.getUser(user_id)
    #user does not exist, create user, create conversation, ask for user type first
    if(fbuser is None):
        fbuser = UserService.create_new_user(user_info,user_id)
        conversation = UserService.create_new_conversation(fbuser)
        return MSG_ASK_FOR_USER_TYPE
    #user exist, so must conversation. Get conversation
    conversation = UserService.get_conversation(fbuser)
    msg = message['message']['text']
    #if the question is user type, check if the user answers with user type
    if(conversation.question == Question.get_question_type('USER_TYPE')):
        fbuser_type = AnswerService.getUsertype(msg)
        #user did not answer with his user type
        if (fbuser_type is None):
            return MSG_ASK_FOR_USER_TYPE
        else:
            #record user type
            fbuser.set_user_type(fbuser_type)
            #TODO: ask next question about email
            conversation.set_conversation_question(Question.get_question_type('NOTHING'))
            return "Okay! You are a " + fbuser_type + ". I'm supposed to ask you about email now, but the code is not there yet"
    #if the question is empty, the msg must be a question
    elif(conversation.question == Question.get_question_type('NOTHING')):
        return "You asked me something, but I don't know how to answer yet"
    return msg

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
                    answer = logic(request, message)
                    post_facebook_message(message['sender']['id'], answer)
        return HttpResponse()
