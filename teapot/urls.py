"""
URL configuration for teapot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from helper.views import render_markdown_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('helper/', include('helper.urls')),
    # path('', home, name='home'),
    path('', lambda request: render_markdown_page(request, 'home'), name='home'),
    path('terms/', lambda request: render_markdown_page(request, 'terms'), name='terms'),
    path('privacy/', lambda request: render_markdown_page(request, 'privacy'), name='privacy')
]
