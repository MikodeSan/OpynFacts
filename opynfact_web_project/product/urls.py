from django.conf.urls import url

from . import views

app_name = 'product'
urlpatterns = [
    url(r'^$', views.index, name='home'), # "/product" will call the method "listing" in "views.py"
    url(r'^index/$', views.index), 
    url(r'^home/$', views.index), 
    url(r'^result/$', views.result, name='result'), 
    url(r'^favorite/$', views.favorite, name='favorite'), 
    url(r'^(?P<_product_id>[0-9]+)/$', views.product, name='info'),
    # url(r'^search/$', views.search),
]