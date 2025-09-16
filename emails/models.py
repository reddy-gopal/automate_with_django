from django.db import models
from ckeditor.fields import RichTextField

class List(models.Model):
    email_list = models.CharField(max_length=100)

    def __str__(self):
        return self.email_list
    
class Subscriber(models.Model):
    email_address = models.EmailField()
    list = models.ForeignKey(List, on_delete=models.CASCADE , related_name= 'subscribers')

    def __str__(self):
        return f'{self.email_address} subscribed the list {self.list.email_list}'
    

class Email(models.Model):
    email_list = models.ForeignKey(List , on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = RichTextField()
    attachment = models.FileField(upload_to= 'email_attachments/')
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

