"""Games URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from chess import views as chess_views
from chat import views as chat_views
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('chess.urls')),
    path('about/', chess_views.about, name='about'),
    path('login/', chess_views.login, name='login'),
    path('logout/', chess_views.logout, name='logout'),
    path('join/', chess_views.join, name='join'),
    path('room/', chess_views.room, name='room'),
    path('tic/', chess_views.tic, name='tic'),
    path('board/', chess_views.board, name='board'),
    path('reset/', chess_views.reset, name='reset'),
    path('chat/', include('chat.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
