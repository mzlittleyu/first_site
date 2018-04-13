# CODING=UTF-8
from django import forms
from .models import ArticleColumn,ArticlePost,ArticleComments
class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title","body",)
class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComments
        fields = ("body",)
