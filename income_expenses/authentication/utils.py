from django.core.mail import send_mail, EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(
            subject=data['email_subject'],
            body = data['email_body'],
            to = [data['to_email'],]
        )
        email.send()