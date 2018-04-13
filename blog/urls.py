from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.get_BlogTltle, name="get_BlogTltle"),
    url(r'(?P<article_id>\d)/$',views.get_BlogContents,name="blog_detail"),
]