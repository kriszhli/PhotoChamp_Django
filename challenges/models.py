from django.db import models
from django.urls import reverse

class Challenge(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    description = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField()
    tags        = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('challenges:detail', args=[self.slug])
