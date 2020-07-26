from django.db import models
from datetime import date,datetime
from django.contrib.auth.models import User





# Create your models here.
class Tags(models.Model):
    tags = models.CharField( max_length = 10)
    
    def __str__(self):
        return self.tags

class Post(models.Model):
    images = models.ImageField(upload_to='images/',blank=True,null=True)
    description = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=datetime.now,blank=True,null=True)
    tags = models.ManyToManyField(Tags,related_name="post_tags",blank=True,null=True)
    likes = models.ManyToManyField(User,related_name="post_likes",blank=True,null=True)
    dislikes = models.ManyToManyField(User,related_name="post_dislikes",blank=True,null=True)
    
    def __str__(self):
        return self.description
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()


