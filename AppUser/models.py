from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    college_name = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True, help_text="List your skills separated by commas")
    portfolio_link = models.URLField(blank=True, null=True)
    
    # We'll link the resume to the user
    current_resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    resume_raw_text = models.TextField(blank=True)
    current_skills_projects = models.TextField(blank=True)