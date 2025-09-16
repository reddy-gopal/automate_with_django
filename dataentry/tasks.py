import os

from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from awd_main import settings

@app.task
def celery_testing():
    time.sleep(10)
    mail_subject = 'Testing the email'
    message = 'This is from mail Trap'
    from_email = settings.EMAIL_HOST_USER
    to_email = 'gopalreddyanthapu07@gmail.com'
    mail = EmailMessage(mail_subject, message, from_email , to= [to_email])
    mail.send()
    return 'Email Sent successfullyy'

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path , model_name)
        mail = EmailMessage(
            subject='Data Imported Successfully',
            body=f'The data import for {model_name} was successful.',
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_RECIEVER]
        )
        mail.send()
    except Exception as e:
        raise e
    return "Inserted Successfully"


from dataentry.utils import exported_file
@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    
    file_path = exported_file(model_name)
    mail = EmailMessage(
            subject='Data Exported Successfully',
            body=f'The data export for {model_name} was successful.',
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_RECIEVER]
    )
    mail.attach_file(file_path)
    mail.send()
    return 'Exported Successfully'