from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage

@app.task
def celery_testing():
    time.sleep(10)
    mail_subject = 'Testing the email'
    message = 'This is from mail Trap'
    from_email = 'gopalreddyanthapu@gmail.com'
    to_email = 'gopalreddyanthapu007@gmail.com'
    mail = EmailMessage(mail_subject, message, from_email , to= [to_email])
    mail.send()
    return 'Email Sent successfullyy'

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path , model_name)
    except Exception as e:
        raise e
    return "Inserted Successfully"



@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    return 'Exported Successfully'