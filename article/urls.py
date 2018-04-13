from django.conf.urls import url
from . import views,list_views
urlpatterns = [
    url(r'^article-column/$',views.articles_column,name= 'article_column'),
    url(r'^rename-article/$',views.rename_article_column,name="rename_article_column"),
    url(r'^del-column/$',views.delete_column,name="del_article_column"),
    url(r'^article-post/$',views.article_post,name='article_post'),
    url(r'^article-list/$',views.article_list,name='article_list'),
    url(r'^article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.article_detail,name = "article_detail"),
    url(r'^del-article/$',views.del_article,name='del_article'),
    url(r'^edit-article/(?P<article_id>\d+)/$',views.edit_article,name= "edit_article"),
    url(r'^list-article-titles/$',list_views.article_titles,name='article_titles'),
    url(r'^list-article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',list_views.article_detail,name='list_article_detail'),
    url(r'^author-article-list/(?P<author_id>\d+)/$', list_views.author_article_list, name='author_article_list'),
    url(r'^like-article/', list_views.like_article, name='like_article'),
]