from json import dumps, loads
from pprint import pprint
from bot_email.emailbot import Email
import requests
import facebook

# Permanent page access token
# TODO change access token to production one before pushing.
PAGE_ACCESS_TOKEN = 'EAAFJaTQTZCAgBAKquTNCRxUz2edEmSuocZC9EreThZAiGFImZAHGGqVlcLdvRDe3vMNXZBvXnQL3ZC0VMJY8IMAWt6t0j8tZCBwsYBZAQDEYOh1kwdjzmnu6zkg1tPyWITWTtgcQvZAw0mvyqZAIkZABmmkMQr1UQwBCkKkcXCTmaZAFHAZDZD'
#PAGE_ACCESS_TOKEN = 'EAAVTNRkgcFgBAAjnZCK6PjN9kWSFrR086wPA8aEqZBYlCCHvtgB8WZCWcjrZAaVEQ1eMJUnjQR9kD0zly4cPYRJnKmoT3jD92oY4EN77qsH6LJXMJ0DsRGdBbIKzXhBzAeXC3o80ZAMYzbhZBEA79SVXiwsWWSMqmkuQHJhcarUwZDZD'
graph = facebook.GraphAPI(PAGE_ACCESS_TOKEN, version='2.2')

class CommunicationService:
    def get_user_info(user_id):
        user = requests.get(("https://graph.facebook.com/v2.6/%s?access_token=%s" % (user_id, PAGE_ACCESS_TOKEN)))
        return user

    def post_facebook_message(fbid, received_message):
        # TODO Change access token
        post_message_url = 'https://graph.facebook.com/v2.8/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
        response_msg = dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        print('SEND STATUS')
        pprint(status.json())
