import smtplib
from email.message import EmailMessage

from core.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from tasks import worker


def get_email_send_code(email: str, code: str):
    email_message = EmailMessage()
    email_message['Subject'] = 'BOFGaming Security Code'
    email_message['From'] = SMTP_USER
    email_message['To'] = SMTP_USER
    email_message.set_content(code)
    return email_message


@worker.task(queue='default')
def send_email_code(email: str, code: str):
    email_message = get_email_send_code(email, code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email_message)
