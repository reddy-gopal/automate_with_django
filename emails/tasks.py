from awd_main.celery import app
from django.conf import settings
from django.core.mail import EmailMessage
from .models import Email, Subscriber

@app.task
def sending_bulk_emails(id):
    email = Email.objects.get(pk = id)
    email_list = email.email_list
    email_addresses = Subscriber.objects.filter(list=email_list)
    emails_list = [sub.email_address for sub in email_addresses]
            
    mail = EmailMessage(
        subject=email.subject,
        body=email.body,
        from_email=settings.EMAIL_HOST_USER,
        to=emails_list
    )

    if email.attachment:
        mail.attach_file(email.attachment.path)

    mail.send()
    return "Emails Sended Successfully.."

