from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='home'), # "/product" will call the method "listing" in "views.py"
    url(r'^index/$', views.index), 
    url(r'^home/$', views.index), 
    url(r'^result/$', views.result, name='list'), 
    url(r'^favorite/$', views.favorite, name='list'), 
    url(r'^account/$', views.account, name='account'), 
    url(r'^(?P<_product_id>[0-9]+)/$', views.product, name='info'),
    # url(r'^search/$', views.search),
]