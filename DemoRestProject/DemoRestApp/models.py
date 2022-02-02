from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Author(models.Model):
    name=models.CharField(max_length=101)
    email=models.EmailField()
    
    def __str__(self):
        return self.name
class Article(models.Model):
    title=models.CharField(max_length=121)
    description=models.TextField()
    body=models.TextField()
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
class User(AbstractUser):
    phone=models.CharField(max_length=11)
    password2=models.CharField(max_length=51)