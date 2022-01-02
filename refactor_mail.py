import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"
LOGIN = 'login@gmail.com'
PASSWORD = 'qwerty'


class Mail:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send_message(self, recipients: list, subject: str, text: str):
        message = MIMEMultipart()
        message['From'] = self.login
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(text))

        message_server = smtplib.SMTP(GMAIL_SMTP, 587)  # identify ourselves to smtp gmail client
        message_server.ehlo()  # secure our email with tls encryption
        message_server.starttls()  # re-identify ourselves as an encrypted connection
        message_server.ehlo()
        message_server.login(self.login, self.password)

        message_server.sendmail(self.login, message_server, message.as_string())
        message_server.quit()

    def recieve_message(self, folder: str, message_subject: str or None):
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select(folder)
        if message_subject:
            criterion = f'(HEADER Subject {message_subject})'
        else:
            criterion = 'ALL'

        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message

if __name__ == '__main__':
    my_email = Mail(login=LOGIN, password=PASSWORD)

    subject = 'Subject'
    recipients = ['vasya@email.com', 'petya@email.com']
    message = 'Message'
    my_email.send_message(recipients=recipients, subject=subject, text=message)

    message_subject = None
    folder = "inbox"
    message_text = my_email.recieve_message(folder=folder, message_subject=message_subject)