from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'account'
urlpatterns = [
    path('<int:user_id>', views.profil, name='profile'),
    path('sign-up/id', views.signup, name='signup'),     # register
    path('sign-up/key', views.signup_password, name='signup-pwd'),
    path('sign-in', views.connect, name='signin'),
    path('logon', auth_views.LoginView.as_view()),
    path('sign-out', views.disconnect, name='signout'),
    # re_path(r'^connection$', views.connect, name='connection'),
]

# re_path(r'^accueil', views.home),
# re_path(r'^article/(?P<id_article>.+)', views.view_article), 
# re_path(r'^articles/(?P<tag>.+)', views.list_articles_by_tag), 
# re_path(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})', views.list_articles),  