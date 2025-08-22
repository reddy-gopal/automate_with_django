from django.core.mail import EmailMessage   
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from .models import List
from emails.tasks import sending_bulk_emails
def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)

            email_list_id = request.POST.get('email_list')
            email_list = List.objects.get(pk=email_list_id)
            print(email_list)

            form.email_list = email_list
            form.save() 
            print(form.id)

            
            try:
                sending_bulk_emails.delay(form.id)

            except Exception as e:
                raise e

            messages.success(request, "Emails are Sending .. scroll insta for a while , you will be notified once it is done")
            return redirect('send_email')
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})
