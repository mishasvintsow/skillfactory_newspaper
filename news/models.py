from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)
    
    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()
        
class Category(models.Model):
    name = models.CharField(max_length = 64, unique = True)
    
    
class Post(models.Model):
    article = 'a'
    news = 'n'
    
    POST_TYPE = [
        (article, "Статья"),
        (news, "Новость")
    ]
    
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    post_type = models.CharField(max_length = 1, choices = POST_TYPE, default = article)
    created = models.DateTimeField(auto_now_add = True)
    cats = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 256)
    text = models.TextField()
    rating = models.IntegerField(default = 0)
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()
        
    def preview(self):
        size = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:size]+'...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()