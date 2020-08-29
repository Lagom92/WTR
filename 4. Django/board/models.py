from django.db import models

# Create your models here.
class Webtoon(models.Model):
    wt_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    score = models.CharField(max_length=50)
    writer = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    summary = models.TextField()
    link = models.CharField(max_length=500)
    
    def __str__(self):
        return self.title