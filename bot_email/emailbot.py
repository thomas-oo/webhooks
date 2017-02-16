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

    #Connects to gmail smtp server and send email genereted by generate_email()
    #@return void - email sent
    def send_email(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.src, self.password)
        msg = self.generate_email()
        try:
            server.sendmail(self.src, self.dest, msg)
        except smtplib.SMTPRecipientsRefused:
            print('received invalid email address' + self.dest)
        server.quit()

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
