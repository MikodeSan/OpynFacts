from django.conf.urls import url
from django.urls import path, re_path

from . import views


app_name = 'product'
urlpatterns = [
    # url(r'^index/$', views.index), 
    # url(r'^home/$', views.index), 
    path('', views.index, name='home'),
    # re_path(r'^result/$', views.result, name='result'),
    path('result/<str:user_query>', views.result, name='result'),
    path('favorite', views.favorite, name='favorite'),
    path('parse/favorite', views.parse_favorite, name='parse_favorite'),
    # url(r'^(?P<_product_id>[0-9]+)/$', views.product, name='info'),
    path('product/<int:product_id>/from/<str:page_origin>', views.product, name='product'),
    path('product/<int:product_id>/from/<str:page_origin>/<str:product_id_origin>', views.product, name='product'),
    # url(r'^notices/$', views.notice, name='notice'),
    path('notices', views.notice, name='notice'),
    ]