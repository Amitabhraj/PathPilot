from django.contrib import admin
from django.urls import include, path
from AppResume.UseCases import upload_resume
from .UseCases import *

urlpatterns = [
    path('upload-resume/', upload_resume.upload_resume, name='upload_resume')
]
