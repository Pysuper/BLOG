from user.models import Ouser
from storm.models import Article, Tag, Category
from .serializers import (UserSerializer, ArticleSerializer, TagSerializer, CategorySerializer)
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.shortcuts import render

# RESEful API VIEWS
class UserListSet(viewsets.ModelViewSet):
    queryset = Ouser.objects.all()  # 指定查询集
    serializer_class = UserSerializer  # 指定serializer序列化器
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)  # 登陆者的权限，是Admin还是普通用户，是Admin可以访问还是普通用户可以访问=> 写入时的权限校验


class ArticleListSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagListSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class CategoryListSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

def parse_seo(request):
    return render(request, 'baidu_verify_cB89BMWgbu.html')
