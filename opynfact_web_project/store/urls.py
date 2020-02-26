from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.listing), # "/store" will call the method "listing" in "views.py"
]