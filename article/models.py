from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from slugify import slugify
# Create your models here.
class ArticleColumn(models.Model):
    user = models.ForeignKey(User,related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.column
class ArticlePost(models.Model):
    author = models.ForeignKey(User,related_name='article')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn,related_name='article_column')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User,related_name="article_like",blank=True)
    class Meta:
        ordering = ('-updated',)
        index_together = (('id','slug'),)
    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id,self.slug])
    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.id, self.slug])
class ArticleComments(models.Model):
    article = models.ForeignKey(ArticlePost,related_name="comments")
    commentator = models.ForeignKey(User,related_name="user_all_comments")
    body = models.CharField(max_length=100)#为什么不能用TextField？
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)

