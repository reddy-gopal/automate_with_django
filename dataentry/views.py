from django.shortcuts import render, redirect
from django.http import HttpResponse

from uploads.models import Upload
from django.apps import apps

def get_all_custom_models():
    default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission']
    custom_models = []
    for model in apps.get_models():
        if model.__name__ in default_models:
            continue
        custom_models.append(model.__name__)
    return custom_models


from django.conf import settings
from django.core.management import call_command
from django.contrib import messages
def import_data(request):
    all_models = get_all_custom_models()
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(file = file_path , model_name = model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        file_path = base_url + relative_path
        try:
            call_command('importdata', file_path , model_name)
            messages.success(request, "Data inserted Successfully")
        except Exception as e:
            messages.error(request , str(e))

        
        return redirect('import')

        
    return render(request , 'importdata.html', {"models" : all_models})


def home(request):
    return HttpResponse("Welcome..")