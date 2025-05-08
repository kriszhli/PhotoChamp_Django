from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    def profile_image_path(instance, filename):
        return f'profiles/{instance.user.username}/images/{filename}'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to=profile_image_path, blank=True, null=True)
    bio  = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class VisitCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    last_visit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'}: {self.count}"
