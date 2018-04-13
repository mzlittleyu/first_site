# CODING=UTF-8
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render
from .models import ArticlePost,ArticleColumn,ArticleComments
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import redis
from .forms import CommentForm
from django.conf import settings
r = redis.StrictRedis(host = settings.REDIS_HOST,port = settings.REDIS_PORT,db = settings.REDIS_DB)
def article_titles(request):
    articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title,3)
    page = request.GET.get('page')
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,"article/list/article_titles.html",{"articles":articles,"page":current_page,"most_viewed":most_viewed})
@csrf_exempt
def article_detail(request,id,slug):
        article = get_object_or_404(ArticlePost,id = id,slug = slug)
        total_views = r.incr("article:{}:views".format(article.id))
        r.zincrby('article_ranking',article.id,1)
        article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
        article_ranking_ids = [int(id) for id in article_ranking]
        most_viewed = list(ArticlePost.objects.filter(id__in = article_ranking_ids))
        most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
        if request.method == "GET":
            comment_form = CommentForm()
            return render(request, "article/list/list_article_detail.html",
                          {"article": article, "total_views": total_views, "most_viewed": most_viewed,
                           "comment_form": comment_form})
        else:
            if request.user.is_authenticated:
                comment = request.POST['comment']
                if comment:
                    commentator_id = request.user.id
                    article_id = article.id
                    ArticleComments.objects.create(body=comment,article_id = article_id,commentator_id = commentator_id)
                    return HttpResponse("1")
                else:
                    return HttpResponse("2")
            else:
                return HttpResponse("3")
def author_article_list(request,author_id):
    try:
        user = User.objects.get(id= author_id)
        userinfo = user.userinfo
    except:
        userinfo=None
    articles_list = ArticlePost.objects.filter(author_id=author_id)
    paginator = Paginator(articles_list,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,"article/list/author_article_list.html",{"articles":articles,"page":current_page,"userinfo":userinfo,"user1":user})
@csrf_exempt
@require_POST
#login_required(login_url='/account/login/')#假如有这个要求，反而会让它不能自动跳转且导致POST提交失败，不合理。
def like_article(request):
        article_id = request.POST.get("id")
        action = request.POST.get("action")
        if article_id and action:
            if request.user.is_authenticated:
                    try:
                        article = ArticlePost.objects.get(id = article_id)
                        if action == "like":
                            article.users_like.add(request.user)
                            return HttpResponse("1")
                        else:
                            article.users_like.remove(request.user)
                            return HttpResponse("2")
                    except:
                        return HttpResponse("nothing")
            else:
                return HttpResponse("3")
        else:
            return HttpResponse("nothing")