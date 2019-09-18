import xadmin
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from storm.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap
from storm.feeds import AllArticleRssFeed

from rest_framework.routers import DefaultRouter
from api import views as api_views

if settings.API_FLAG:
    router = DefaultRouter()
    router.register(r'users', api_views.UserListSet)
    router.register(r'articles', api_views.ArticleListSet)
    router.register(r'tags', api_views.TagListSet)
    router.register(r'categorys', api_views.CategoryListSet)

# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'tags': TagSitemap,
    'categories': CategorySitemap
}

urlpatterns = [
                  url(r'^admin/', xadmin.site.urls, name="xadmin"),
                  # 用户
                  url(r'^accounts/', include('user.urls', namespace='accounts')),
                  # storm
                  url('', include('storm.urls', namespace='blog')),  # blog
                  # 评论
                  url(r'^comment/', include('comment.urls', namespace='comment')),  # comment
                  url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
                  # 网站地图
                  url(r'^feed/$', AllArticleRssFeed(), name='rss'),  # rss订阅
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件

if settings.API_FLAG:
    urlpatterns.append(url(r'^api/v1/', include(router.urls, namespace='api')))  # restframework
