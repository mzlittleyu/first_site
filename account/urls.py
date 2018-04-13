# CODING=UTF-8
from django.conf.urls import url
from . import views
from django.conf import settings
from django.contrib.auth import views as au_views

urlpatterns = [
    url(r'^login/$',au_views.login, name="user_login"),#内置的用户登录
    #url(r'^another_login/$',au_views.login, {"template_name":"account/login.html"}),#内置的第二种用户登录方式
    #url(r'^loginn/$',views.user_login,name="user_login"),#自己设置的用户登录
    url(r'^logout/$',au_views.logout,{"template_name":"account/logout.html"},name="user_logout"),
    #url(r'^register2/$',views.register2,name="user_register"),
    url(r'^register/$',views.register,name="user_register"),
    url(r'^password-change/$',au_views.password_change,{"post_change_redirect":"/account/password_change_done"},name="password_change"),
    url(r'^password_change_done/$',au_views.password_change_done,name="password_change_done"),
    url(r'^password-reset/$',au_views.password_reset,{"post_reset_redirect":"/account/password-reset-done"},name="password_reset"),
    url(r'^password-reset-done/$',au_views.password_reset_done,name="password_reset_done"),
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',au_views.password_reset_confirm,{"post_reset_redirect":"/account/password-reset-complete"},name="password_reset_confirm"),
    url(r'^password-reset-complete/$',au_views.password_reset_complete,name="password_reset_complete"),
    url(r'^my-information/$',views.myself,name="my_information"),
    url(r'^edit-my-information/$',views.edit_myself,name="edit_my_information"),
    url(r'^my-image/$',views.my_image,name ="my_image"),
    url(r'^register_test/$',views.register_test,name="user_register_test"),
    url(r'^home/$',views.arriving_at_homepage2,name='home_test'),
    ]