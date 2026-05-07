from django.db import models

# Create your models here.
class UserResume(models.Model):
    user = models.ForeignKey('AppUser.User', on_delete=models.CASCADE,null=True)
    ats_resume = models.FileField(upload_to='resumes/')
    ats_resume_raw_text = models.TextField(blank=True)
    ats_score = models.IntegerField(default=0)
    suggestions = models.TextField(blank=True)  # Store AI feedback here
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} - Score: {self.ats_score}"
    
