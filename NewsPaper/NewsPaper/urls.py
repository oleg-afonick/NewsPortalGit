"""NewsPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from news import views, tasks

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('timezone/', views.get_session_timezone, name="get_session_timezone"),
    path('tasks1/', tasks.MyTasks1.as_view()),
    path('tasks2/', tasks.MyTasks2.as_view()),
]

admin.site.site_header = 'Администрирование News Portal'
admin.site.index_title = 'Новостной портал'

handler403 = 'news.views.handler403'
