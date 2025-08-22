from django.urls import path

from . import views
urlpatterns = [
    path('import_data/', views.import_data, name= 'import'),
    path('home/', views.home, name= 'home'),
    path('celery_test/', views.celery_task_test),
    path('export_data/', views.export_data , name= 'export_data'),
    path('', views.login, name='login'),
]