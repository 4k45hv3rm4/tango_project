from django.conf.urls import url
from .views import index,show_category

urlpatterns =[
    url(r'^$', index, name="index" ),
    url(r'^category/(?P<category_url>[\w\-]+)$', show_category, name="category")
]
