from django.conf.urls import url
from .views import all_news, create_news, news, search
urlpatterns = [
    url(r'^$', all_news, name = 'all_news'),
    url(r'^create-news', create_news, name = 'create_news'),
    url(r'^news/(?P<id>\d+)/$', news, name = 'news_detail'),
    url(r'^search/$', search, name = 'search')
]
