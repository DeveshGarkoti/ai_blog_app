from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_title = models.CharField(max_length=300)
    youtube_link = models.URLField()
    views = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    publish_date = models.CharField(max_length=20)

    def __str__(self):
        return self.youtube_title