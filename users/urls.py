from django.conf.urls import url
from .views import signup, login_user, logout_user
app_name = 'users'
urlpatterns = [
    url(r'^signup', signup, name = 'signup'),
    url(r'^login', login_user, name = 'login'),
    url(r'^logout', logout_user, name = 'logout'),
]
