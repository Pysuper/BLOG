import markdown
import time
from django.views import generic
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import render, HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, BigCategory, Category, Tag
from markdown.extensions.toc import TocExtension  # 锚点的拓展
from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet


class IndexView(generic.ListView):
    """首页视图，继承子ListView，用于展示从数据库中获取的文章列表"""
    model = Article  # 获取数据库中的文件列表
    template_name = "index.html"  # 用于指定使用哪个模板文件进行渲染
    context_object_name = "articles"  # 用于给上下文变量取名（在模板中使用改名字）
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()  # 重写通用视图的 get_queryset 函数，获取定制数据
        year = self.kwargs.get('year', 0)  # 日期归档
        month = self.kwargs.get('month', 0)
        tag = self.kwargs.get("tag", 0)  # 标签
        self.big_slug = self.kwargs.get('big_slug', '')  # 导航条
        slug = self.kwargs.get('slug', '')  # 文章分类

        if self.big_slug:
            big = get_object_or_404(BigCategory, slug=self.big_slug)
            queryset = queryset.filter(category_bigcategory=big)
            if slug:
                slu = get_object_or_404(Category, slug=slug)
                queryset = queryset.filter(category=slu)

        if year and month:
            queryset = get_list_or_404(queryset, create_date__yrar=year, create_data__month=month)

        if tag:
            tags = get_object_or_404(Tag, name=tag)
            self.big_slug = BigCategory.objects.filter(category__acticle__tags=tags)
            self.big_slug = self.big_slug[0].slug
            queryset = queryset.filter(tags=tags)

        return queryset

    def get_context_data(self, **kwargs):
        """
        1. 在视图函数中将模板变量传递给模板是通过给 render 函数的 content 参数传递一个字典实现的
        2. 例如：render(request, 'blog/index.html', context={'post_list': post_list})
        3. 这里传递了一个 {'post_list': post_list} 字典给模板
        4. 在类视图中，这个需要传递的模板变量，字典是通过 get_context_data 获得的
        5. 所以你要复写该方法，方便再插入一些自定义的模板变量进去
        :param kwargs:
        :return:
        """

        # 首先获取去父类生成的传递给模板的字典
        context = super(IndexView, self).get_context_data(**kwargs)

        """
        父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量
            paginator：Paginator的一个实例
            page_obj：Page的一个实例
            is_paginated：一个布尔变量，用于只是是否分页
                例如：如果规定每页只显示10条数据，而本身只有5条数据，就不需要分页，此时 is_paginated=False
        由于 context 是一个字典，使用 get 方法从中取值
        """
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获取显示分页导航条需要的数据：
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页当好的模板变量更新到 context 中，注意：pagination_data 方法返回的也是一个字典
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板
        # 注意此时 context 字典中已有了显示分页导航条所需要的数据
        context['category'] = self.big_slug
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}
        left = []  # 当前也左边连续的页码号，初始值为空
        right = []  # 当前也右边连续的页码好，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示 最后一页 页码前是否需要显示省略号

        # 标示是否需要显示第 1 页的页码号
        # 因为如果当前页左边的连续页码中已经含有第 1 页的页码号，此时就不用再显示第 1 页的页码号
        # 其他情况下第一页的页码是始终显示的
        first = False
        last = False  # 标示是否需要显示最后一页的页码号， 同上

        page_number = page.number  # 获取当前用户请求的页码
        total_pages = paginator.num_pages  # 获取分页后的总页数

        page_range = paginator.page_range  # 获取整个分页页码列表 ==> 分了四页-[1, 2, 3, 4]

        if page_number:
            """
            如果用户请求的是第一页的数据，那么当前也左边的不需要数据，因此 left = [](默认为空)
            此时只要获取当前也右边的连续页码号
                比如分页页码列表：[1, 2, 3, 4] ==> 获取的就是right=[2, 3]
                注意：这里只获取了当前页码后的两个连续页码，可以更改这个数字以获取更多页码
            """
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减一 还要小
            # 说明最右边的页码号和最后一页的页码号之间还有其他页码，因此需要显示省略号，通过 right_has_more 来表示
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的页码号中不包括最后一页的页码
            # 所以需要显示最后一页的页码号，通过last来标示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[](默认为空)
            # 此时只要获取当前也左边的连续页码号
            # 比如分页页码列表：[1, 2, 3, 4], 那么获取的就是 left = [2， 3]
            # 这里只获取了当前页码后两个连续页码，可以更改这个数字以获取更多页码
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大
            # 说明最左边的页码号和第 1 页的页码号之间还有其他页码，影刺需要显示省略号，通过 left_has_more 来表示
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第 1 页的页码
            # 所以需要显示第一页的页码号，通过 first 来标示
            if left[0] > 1:
                first = True

        else:
            # 用户请求的既不是最后一页，也不是第一页，则需要获取当前页左右两边的连续页码号
            # 这里只获取当前页码号前后两个连续页码，可以更改这个数字以获取更多页码
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第一页和第一页之后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }

        return data


class DetailView(generic.DetailView):
    """Django有基于类的视图DetailView，用于显示宇哥对象的详情页，直接继承它"""
    model = Article  # 获取数据库中的文章列表
    template_name = 'article.html'  # 指定使用那个模板进行渲染
    context_object_name = 'article'  # context_object_name 用于给上下文取名(在模板中使用该名字)

    def get_object(self):
        obj = super(DetailView, self).get_object()
        # 设置浏览器增加时间判断，同一篇文章两次浏览超过半小时才重新统计阅览量，作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:
                    obj.update_views()
                    ses[the_key] = time.time()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        obj.body = md.convert(obj.body)
        obj.toc = md.toc
        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['category'] = self.object.id
        return context


def MessageView(request):
    return render(request, 'message.html', {'category': 'message'})


def LinkView(request):
    return render(request, 'link.html')


def AboutView(request):
    return render(request, 'about.html', {'category': 'about'})


def DonateView(request):
    return render(request, 'donate.html', {'category': 'donate'})


def ExchangeView(request):
    return render(request, 'question.html', {'category': 'question'})


def ProjectView(request):
    return render(request, 'project.html', {'category': 'project'})


def QuestionView(request):
    return render(request, 'question.html', {'category': 'question'})


@csrf_exempt
def LoveView(request):
    data_id = request.POST.get('um_id', '')
    if data_id:
        article = Article.objects.get(id=data_id)
        article.loves += 1
        article.save()
        return HttpResponse(article.loves)
    return HttpResponse('ERROR', status=405)


# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    context_object_name = 'search_name'  # 返回搜索结果集

    # 设置分页
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    queryset = SearchQuerySet().order_by('-views')  # 搜索结果以浏览量排序


def page_not_found(request):
    return render_to_response('404.html')
