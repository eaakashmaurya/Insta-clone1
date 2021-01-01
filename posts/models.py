"""Posts models."""

# Django
from django.db import models
#from django.contrib.auth.models import User
from users.models import Profile


class Post(models.Model):
    """Post Model."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username"""
        return "{} by @{}".format(self.title, self.profile.user.username)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
