"""Servdoudou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views import static
from django.views.generic import TemplateView

import servdou.urls as api_handlers

urlpatterns = [
    path('sitepanel/', admin.site.urls),

    url(r'^api/', include(api_handlers)),

    url(r'^$', TemplateView.as_view(template_name="index.html")),

    # 增加以下一行，以识别静态资源
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')

]

# print(settings.STATIC_ROOT)
