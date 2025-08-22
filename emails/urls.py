from django.urls import path
from . import views
urlpatterns = [
    path('send-emails/', views.send_email , name = 'send_email')
]