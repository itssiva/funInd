"""funLtd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', 'user_auth.views.signup', name='signup'),
    url(r'^signin/$', 'user_auth.views.signin', name='signin'),
    url(r'^signout/$', 'user_auth.views.signout', name='signout'),
    url(r'^reset/$', 'user_auth.views.reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'user_auth.views.reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'user_auth.views.success', name='success'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'user_auth.views.activate_account', name='activate'),
    url(r'^profile/(?P<username>[0-9A-Za-z_\-]+)', 'user_auth.views.profile','profile')


]
