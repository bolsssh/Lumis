import smtplib as smtp
from getpass import getpass

email = 'JikBig@yandex.ru'
password = "EasyPasswordForAlisa2003"


def send_email(dest_email, subject, email_text):
    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                           dest_email,
                                                           subject,
                                                           email_text)
    # message = message.format(email, dest_email, subject, email_text)
    print(email_text)
    server = smtp.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    server.sendmail(email, dest_email, message)
    server.quit()
