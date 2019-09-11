from django.db import models
from django.conf import settings
from django.shortcuts import reverse


# 文章导航菜单栏分类表
class BigCategory(models.Model):
    name = models.CharField(max_length=20, verbose_name="文章大分类")  # 导航名称
    slug = models.SlugField(unique=True)  # 用作文章的访问路径，每篇文章有独一无二的标识
    description = models.TextField(max_length=240, default=settings.SITE_DESCRIPTION, help_text="作为SEO中的description，长度参考SEO标准", verbose_name="描述")  # 分类页描述
    keywords = models.TextField(max_length=240, default=settings.SITE_KEYWORDS, help_text="作为SEO中的keywords, 长度参考SEO标准", verbose_name="关键字")  # 分类页keywords

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "大分类"

# 导航栏，分类下的下拉菜单栏
class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="文章分类")
    slug = models.SlugField(unique=True)    # 用作分类路径，独一无二
    description = models.TextField(max_length=240, default=settings.SITE_DESCRIPTION, help_text="作为SEO优化，长度参考SEO标准")
    bigcategory = models.ForeignKey(BigCategory, verbose_name="大分类")    # 对应导航栏

# 文章关键字，作为SEO的keywords
class KeyWord(models.Model):
    name = models.CharField(max_length=20, verbose_name="文章关键词")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "关键词"
        ordering = ["name"]


# 文章标签
class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name="文章标签")
    slug = models.SlugField(max_length=240, default=settings.SITE_DESCRIPTION, help_text="作为SEO中的description，长度参考SEO标准", verbose_name="描述")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog.tag', kwargs={"tag": self.name})

    def get_article_list(self):
        return Article.objects.filter(tags=self)    # 返回当前标签下所有发表的文章列表

    class Meta:
        verbose_name_plural = verbose_name = "标签"
        ordering = ["id"]
