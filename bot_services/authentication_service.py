from fb_mcbot.models import FBUser
from bot_email.emailbot import Email
from pprint import pprint
import string
import random

class AuthenticationService:

    # the user has not gone through the Authenticationation process yet.
    AUTHENTICATION_NO = 'authentication_no'
    # the bot is waiting for the user to enter McGill email.
    AUTHENTICATION_EMAIL = 'authentication_email'
    # the user entered the invalid email or wrong Authenticationation code, so the bot is waiting for the user to continue or quit.
    AUTHENTICATION_ON = 'authentication_on'
    # the bot is waiting for the user to enter Authenticationation code.
    AUTHENTICATION_WAIT = 'authentication_wait'
    # the user has already gone through the Authenticationation process and is recognized by the bot.
    AUTHENTICATION_DONE = 'authentication_done'

    # Reset a user's Authentication_status back to "no".
    def resetAuthentication(user):
        user.authentication_status = AuthenticationService.AUTHENTICATION_NO
        user.save()

    # Generate random Authenticationation code.
    def idGenerator(size = 6, chars = string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # Run through the Authenticationation process.
    def authenticationProcess(user, input):
        authenticationState = user.authentication_status  # Get Authentication_status of a user.

        if authenticationState == AuthenticationService.AUTHENTICATION_NO:
            # Move to waiting for user's McGill email stage.
            user.authentication_status = AuthenticationService.AUTHENTICATION_EMAIL
            user.save()
            return "Please enter your McGill email:"

        elif authenticationState == AuthenticationService.AUTHENTICATION_EMAIL:
            # Check if it is a valid McGill email.
            if input.endswith("@mail.mcgill.ca") or input.endswith("@mcgill.ca"):
                code = AuthenticationService.idGenerator()  # Generate Authenticationation code.

                # Update user's Authenticationation code and McGill email.
                user.code = code
                user.mcgill_email = input

                # Send email.
                email = Email(user.mcgill_email, 'McBot Confirmation Email')
                email.send_confirmation_email(user.code, user.first_name, user.last_name)

                # Move to waiting for Authenticationation code stage.
                user.authentication_status = AuthenticationService.AUTHENTICATION_ON
                user.save()

                return "Authentication email sent. Please enter your Authentication code:"

            else:
                # Move to waiting for the user to continue or quit stage.
                user.authentication_status = AuthenticationService.AUTHENTICATION_WAIT
                user.save()
                return "Invalid McGill Email. Do you want to quit? (yes/no)"

        elif authenticationState == AuthenticationService.AUTHENTICATION_ON:
            # Check if the Authenticationation code is correct.
            if input == user.code:
                # Move to complete Authenticationation stage.
                user.authentication_status = AuthenticationService.AUTHENTICATION_DONE
                user.save()
                return "The Authenticationation code is correct. Welcome to McBot! You can log out by typing [logout]"

            else:
                # Move to waiting for the user to continue or quit stage.
                user.authentication_status = AuthenticationService.AUTHENTICATION_WAIT
                user.save()
                return "The Authenticationation code is NOT correct. Do you want to quit? (yes/no)"

        elif authenticationState == AuthenticationService.AUTHENTICATION_WAIT:
            # Check if the user enter "yes" or "no".
            if input.lower() == "yes":
                # Move to not going through Authenticationation process stage.
                user.authentication_status = AuthenticationService.AUTHENTICATION_NO
                user.save()
                return "You have quit the Authenticationation process."

            elif input.lower() == "no":
                # Move to waiting for user's McGill email stage.
                user.authentication_status = AuthenticationService.AUTHENTICATION_EMAIL
                user.save()
                return "Please enter your McGill email:"

            else:
                # If the user entered something other than "yes" or "no", repeat the question.
                return "Do you want to quit? (yes/no)"

        else:
            # Show the message if the user has already gone through the Authenticationation process.
            return "You have already finished Authentication."
