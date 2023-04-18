from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone 

# Create your models here.

class Author(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.EmailField(max_length=255)

    def full_name(self)->str:
        return f"{self.first_name} {self.last_name}"


    def __str__(self) -> str:
        return self.full_name()



class Post(models.Model):
    title=models.CharField(max_length=255)
    excerpt=models.CharField(max_length=255)
    # image_name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='images',null=True)
    date=models.DateField(auto_now_add=True)
    content=models.TextField()
    slug=AutoSlugField(populate_from='title',unique=True)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,related_name='posts',null=True)
    tags=models.ManyToManyField('Tag')

    def __str__(self)->str:
        return self.title

class Tag(models.Model):
    caption=models.CharField(max_length=255)

    def __str__(self)->str:
        return self.caption
    

class Comment(models.Model):
    user_name=models.CharField(max_length=120)
    email_address=models.EmailField()
    text=models.TextField(max_length=400)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')


