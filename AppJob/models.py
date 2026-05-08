from django.db import models

# Create your models here.
class Questions(models.Model):
    QuestionType = (
        ("DSA", "DSA"),
        ("APTITUDE", "APTITUDE"),
    )
    title = models.CharField(max_length=200)
    url = models.URLField()
    type = models.CharField(default="DSA",choices=QuestionType, max_length=50)
    company = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)

    def __str__(self):
        return self.title + " on " + self.platform
