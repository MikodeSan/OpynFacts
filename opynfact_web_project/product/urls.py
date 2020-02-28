from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index), # "/product" will call the method "listing" in "views.py"
    url(r'^index/$', views.index), 
    url(r'^home/$', views.index), 
    url(r'^result/$', views.result), 
    url(r'^favorite/$', views.favorite), 
    url(r'^account/$', views.account), 
    url(r'^(?P<_product_id>[0-9]+)/$', views.product),
    # url(r'^search/$', views.search),
]