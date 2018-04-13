from django.contrib import admin
from .models import ArticleColumn
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('user','created','column')
    list_filter = ('created',)
# Register your models here.
admin.site.register(ArticleColumn,ArticleColumnAdmin)
