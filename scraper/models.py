from django.db import models
from django.urls import reverse

# Create your models here.
class Serie(models.Model):
    name = models.CharField(max_length=40)
    episode_link = models.CharField(max_length=300, null = True, blank = True)
    episode_num = models.IntegerField(null = True, blank = True)
    season = models.IntegerField()
    last_updated = models.DateTimeField(auto_now = True)

    def get_absolute_url(self):
        return reverse('scraper:tracker')
