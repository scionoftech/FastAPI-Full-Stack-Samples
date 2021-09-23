import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple, List
# import sys
#
# sys.path.append("..")
from app.conf import EmailSettings, ProjectSettings


# Function that send email.
def send_mail(sender_email, password, receiver_email, message):
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(*get_smtp_settings(),
                          context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def email_settings(receiver_email) -> Tuple:
    sender_email = EmailSettings.EMAIL_ID
    password = EmailSettings.EMAIL_PASSWORD

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Instructions"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)

    return sender_email, password, message


def get_smtp_settings() -> Tuple:
    """
    SMTP Server Information
    1. Gmail.com: smtp.gmail.com:587
    2. Outlook.com: smtp-mail.outlook.com:587
    3. Office 365: outlook.office365.com
    Please verify your SMTP settings info.
    """
    return EmailSettings.SMTP_SERVER, EmailSettings.SMTP_PORT


def reset_password_email_content(message, email,
                                 password_reset_token) -> MIMEMultipart:
    # Create the plain-text and HTML version of your message
    link = ProjectSettings.SERVER_HOST + "/reset_password/?code=" + \
           password_reset_token
    text = """\
        Hi,
        We received a request to reset your password for %(email)s. If you didn't make this request, please ignore this email and contact 
        your administrator. Your password has not been reset.
        To reset your password, click on the link below (or copy and paste the URL into your browser):
        %(link)s""" % ({"email": email, "link": link})
    # html = """\
    # <html>
    #   <body>
    #     <p>Hi,<br>
    #        How are you?<br>
    #        <a href="URL">Test Email</a>
    #        has many great tutorials.
    #     </p>
    #   </body>
    # </html>
    # """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    # message.attach(part2)
    return message


def send_reset_password_email(emails: List[str], password_reset_token: str):
    sender_email, password, message = email_settings(emails)
    message = reset_password_email_content(message, emails[0],
                                           password_reset_token)
    send_mail(sender_email, password, emails, message)
