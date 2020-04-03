from django.conf.urls import url
from django.urls import path, re_path

from . import views


app_name = 'product'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    path('notices', views.notice, name='notice'),


    # url(r'^index/$', views.index), 
    # url(r'^home/$', views.index), 
    url(r'^result/$', views.result, name='result'), 
    url(r'^favorite/$', views.favorite, name='favorite'), 
    url(r'^(?P<_product_id>[0-9]+)/$', views.product, name='info'),
    # url(r'^notices/$', views.notice, name='notice'),

    # url(r'^search/$', views.search),
]