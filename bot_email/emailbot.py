import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Email bot class. Send an email as plain text and html format through gmail smtp server. Contains email template.
#@param:
#       dest: destination email
#       title: message subject
class Email():

    def __init__(self, dest, title):
        self.src = 'mcbot428@gmail.com'
        self.password = '2jM73NmlREkbRFsAVNdJL'
        self.dest = dest
        self.title = title
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

    #Connects to gmail smtp server and send test email genereted by generate_email()
    #@return void - email sent
    def send_test_email(self):
        self.start_smtp_server()
        msg = self.generate_email()
        try:
            self.server.sendmail(self.src, self.dest, msg)
        except smtplib.SMTPRecipientsRefused:
            print('received invalid email address: ' + self.dest)
        self.server.quit()

    #Connects to gmail smtp server and send confirmation email.
    #@return void - email sent
    def send_confirmation_email(self, confirmation_code, first_name, last_name):
        self.start_smtp_server()
        msg = self.generate_confirmation_email(confirmation_code, first_name, last_name)
        try:
            self.server.sendmail(self.src, self.dest, msg)
        except smtplib.SMTPRecipientsRefused:
            print('received invalid email address: ' + self.dest)
        self.server.quit()

    #Login into the smtp gmail server. Note the server is passed a class instance variable.
    def start_smtp_server(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.src, self.password)

    #generate email with confirmation code as plain text and html format. Email's template hardcoded within this function.
    #@return email's content as a string.
    def generate_confirmation_email(self, confirmation_code, first_name, last_name):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.title
        msg['From'] = self.src
        msg['To'] = self.dest

        text = "Hi!\nThis is your confirmation code: " + confirmation_code + "\nSimply message the code to McBot to confirm your registration."
        html = """
        <html>
            <head></head>
            <body>
                <p>Hi! """ + first_name + """ """ + last_name + """ <br>
                    <br>
                    This is your confirmation code: <b> """ + confirmation_code + """</b><br>
                    Simply message the code to McBot to confirm your registration.<br>
                    Thank you.<br>
                    <br>
                    McGill McBot Team
                    <br>
                </p>
            </body>
        </html>
        """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        return msg.as_string()

    #generate email as plain text and html format using python email.mime lib. Email's template hardcoded within this function.
    #@return email's content as a string.
    def generate_email(self):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.title
        msg['From'] = self.src
        msg['To'] = self.dest

        text = "Hi!\nThis is a test msg.\nHere is a link: http://example.com"
        html = """
        <html>
            <head></head>
            <body>
                <p>Hi!<br>
                    <b>This is a test msg.</b></br>
                    Here is a link: <a href="http://example.com">example.com</a>
                </p>
            </body>
        </html>
        """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        return msg.as_string()
