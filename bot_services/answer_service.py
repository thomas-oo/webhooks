import re
from bot_services.user_service import UserService, Question
from bot_services.communication_service import CommunicationService

MSG_ASK_FOR_USER_TYPE = 'Are you a [student] or [instructor]?'

class AnswerService:
    #TODO:make it more elegant if possible
    def getUsertype(answer):
        searchObj = re.search(r'\b[Ss]tudent\b',answer)
        if searchObj:
            return 'student'
        else:
            searchObj = re.search(r'\b[Ii]nstructor\b',answer)
            if searchObj:
                return 'instructor'
            else:
                return None

    #business logic
    def process_message(message):
        user_id = (message['sender']['id'])
        user_info = CommunicationService.get_user_info(user_id).json()
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
