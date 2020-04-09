from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from .views import login_view, logout_view, register_view, profile_view, change_profile_view

urlpatterns = [
    url(r'^login/$', login_view, name='login'), # 用户登录
    url(r'^logout', logout_view, name='logout'),    # 用户退出
    url(r'^register/$', register_view, name='register'),    # 用户注册
    url(r'^profile/$', profile_view, name='profile'),   # 用户查看资料
    url(r'^profile/change/$', change_profile_view, name='change_profile'),  # 修改用户资料
    url(r'^api/docs/', include_docs_urls(title="SmallSpider_BLOG API")) # 查看api文档？？？
]