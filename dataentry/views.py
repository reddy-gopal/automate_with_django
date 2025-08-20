from django.shortcuts import render, redirect
from django.http import HttpResponse

from uploads.models import Upload



from django.conf import settings
from django.contrib import messages
from dataentry.utils import get_all_custom_models
from dataentry.tasks import import_data_task
from .utils import check_csv_errors

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
            check_csv_errors(file_path, model_name)
            
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import')

    
        
        import_data_task.delay(file_path, model_name)
        messages.success(request, 'Data is Inserting, Scroll the instagram reels for a while we will notify you After the completion ')
        

        
    return render(request , 'importdata.html', {"models" : all_models})


def home(request):
    return HttpResponse("Welcome..")


from dataentry.tasks import celery_testing

def celery_task_test(request):
    celery_testing.delay()
    return HttpResponse('<h1>Function Runned</h1>')


from dataentry.tasks import export_data_task
def export_data(request):
    all_models = get_all_custom_models()

    if request.method == 'POST':
        model_name = request.POST.get('model_name')

        try:
            export_data_task.delay(model_name)
        except Exception as e:
            raise str(e)
        
        messages.success(request , "Exporting.... please wait")
        redirect('export_data')
    
    return render(request , 'exportdata.html', {"models": all_models})