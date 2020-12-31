"""Posts models."""

# Django
from django.db import models
#from django.contrib.auth.models import User
from users.models import Profile


class Post(models.Model):
    """Post Model."""

    profile = models.ForeignKey(Profile, related_name="posts", null=True, on_delete=models.SET_NULL )

    title = models.CharField(max_length=255) #CAPTION
    photo = models.ImageField(upload_to='posts/photos') 
    
    post_likes = models.ManyToManyField(Profile, default=False, blank=True, related_name="likes")
    #charfield the tag
    #tag_someone = models.ForeignKey(Profile, related_name="tag", blank=True, default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username"""
        return "{} by @{}".format(self.title, self.profile.user.username)