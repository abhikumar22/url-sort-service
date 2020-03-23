from django.db import models

class Urlsortner(models.Model):
    full_url = models.CharField(max_length=1000)
    sort_url = models.CharField(max_length=30)
    no_of_clicks = models.CharField(max_length=30)
