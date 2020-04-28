from django.conf.urls import url
from .views import index,show_category,add_category, add_page,register,user_login,  user_logout



urlpatterns =[
    url(r'^$', index, name="index" ),
    url(r'^add_category/$', add_category, name="add_category"),
    url(r'^add_page/(?P<category_url>[\w\-]+)$', add_page, name="add_page"),
    url(r'^category/(?P<category_url>[\w\-]+)$', show_category, name="category"),
    url(r'^register/$', register, name="register"),
    url(r'^login/$', user_login, name="login"),
    url(r'^logout/$', user_logout, name="logout")

]
