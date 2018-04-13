# CODING=UTF-8
from django import  template
from django.db.models import Count
register = template.Library()
from article.models import ArticlePost
@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()#需要创建objects对象
@register.simple_tag#每个函数都需要
def author_total_articles(user):
    return user.article.count()#不用再创建objects对象了
@register.inclusion_tag('article/list/latest_articles.html')#存在一个地方方便引用
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles":latest_articles}
@register.assignment_tag
def most_commented_articles(n=8):
    return ArticlePost.objects.annotate(total_comments = Count("comments")).order_by("-total_comments")[:n]#先通过Count计算出每篇文章的评论数，并且储存好且赋予其total_comments这个属性，再按照这个属性排序