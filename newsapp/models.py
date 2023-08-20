from django.contrib.auth.models import User
from django.db import models


class UserSearch(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add any additional fields you'd like here, for example:
    # profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username
