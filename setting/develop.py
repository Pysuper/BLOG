import os
import sys
from script import log_theme

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'g=hfy#h-k2$lwq=*4b)vkjg#zpvul2fw*m4pi_c($3tak=ms8j'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # 添加人性化过滤器
    'storm',  # 博客应用
    'user',  # 自定义用户应用
    'comment',  # 评论
    # 'xadmin',  # xadmin
    'crispy_forms',
    'ckeditor',  # 配置富文本编辑器
    'ckeditor_uploader',  # 配置上传图片
    'haystack',  # 全文搜索应用 这个要放在其他应用之前
    'rest_framework',  # API
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'storm.context_processors.settings_info',  # 自定义上下文管理器
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root',
        'NAME': 'BLOG',
        # 避免映射数据库时出现警告
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        #     'charset': 'utf8mb4',
        # },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 媒体文件收集 ==> 富文本编辑器的文件上传路径
MEDIA_URL = "/media/"  # 媒体文件别名(相对路径) 和 绝对路径
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'media')
)
CKEDITOR_UPLOAD_PATH = "article_images"  # 富文本编辑器图片上传的保存路径

# 统一分页设置
BASE_PAGE_BY = 4
BASE_ORPHANS = 5

# 全文搜索应用配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'storm.whoosh_cn_backend.WhooshEngine',  # 选择语言解析器为自己更换的结巴分词
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),  # 保存索引文件的地址，选择主目录下，这个会自动生成
    }
}
# 自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 自定义用户model
AUTH_USER_MODEL = 'user.Ouser'

SITE_DESCRIPTION = "small_spider的个人网站，记录生活的瞬间，分享学习的心得，感悟生活，留住感动，静静寻觅生活的美好"

SITE_KEYWORDS = "Python"

SITE_END_TITLE = "聚会阅读器"

API_FLAG = True

# 配置后台xadmin
XADMIN_TITLE = "TAO BLOG 后台管理"  # 左上方的文字
XADMIN_FOOTER_TITLE = "small.spider.p@gmail.com"  # 最下面的文字

# 配置富文本编辑器
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": 800,
        "tabSpaces": 4,
        "extraPlugins": "codesnippet",  # 配置代码插件
    },
}

# 修改默认存储引擎为自定义的
DEFAULT_FILE_STORAGE = 'blog.storage.WatermarkStoarge'

# 配置ckeditor的js路径
CKEDITOR_JQUERY_URL = 'https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js'

# 将CKEditor需要的媒体资源拷入STATIC_ROOT指定的路径中
STATIC_ROOT = os.path.join(BASE_DIR, 'whoosh_index')

# 添加日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "log/blog.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
