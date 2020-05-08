from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'account'
urlpatterns = [
    path('sign-up/id', views.signup, name='signup'),     # register
    path('sign-up/key', views.signup_password, name='signup-pwd'),
    path('sign-in', views.signin, name='signin'),
    # path('sign-in', views.signin, name='signin'),
    # path('logon', auth_views.LoginView.as_view()),
    path('<int:user_id>', views.profile, name='profile'),
    path('', views.profile, name='profile'),
    path('sign-out/request', views.signout_request, name='signout_request'),
    path('sign-out', views.signout, name='signout'),
    # re_path(r'^connection$', views.connect, name='connection'),
]

# re_path(r'^articles/(?P<tag>.+)', views.list_articles_by_tag), 
# re_path(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})', views.list_articles),  