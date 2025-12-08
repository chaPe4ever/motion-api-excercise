from django.db import models

from post.models import Post


# Create your models here.
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.URLField()

    def __str__(self):
        return f"Image for Post {self.post.id}"
