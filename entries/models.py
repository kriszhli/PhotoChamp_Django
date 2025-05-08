from django.db import models
from django.contrib.auth.models import User
from challenges.models import Challenge

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='entries/%Y/%m/%d/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class EntryReview(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('entry', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review of {self.entry.title} by {self.user.username}"

