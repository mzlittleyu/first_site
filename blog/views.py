from django.shortcuts import render,Http404
from .models import BlogArticles
from django.http import HttpResponse
def get_BlogTltle(request):
    if request.user.id ==1:
        blogs = BlogArticles.objects.all()
        return render(request,"blog/titles.html",{"blogs":blogs})
    else:
        return HttpResponse("哈哈哈，想看管理员的日记！想得美，要是你够聪明就猜密码吧~账号rainbowuuu密码uuuuuu加那个星巴克的数字")
# Create your views here.
def get_BlogContents(request,article_id):
    try:
        article = BlogArticles.objects.get(id = article_id)
    except:
        raise Http404()
    pub = article.publish
    return render(request,"blog/content.html",{"article":article,"publish":pub})