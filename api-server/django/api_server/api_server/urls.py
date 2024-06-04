"""
URL configuration for api_server project.

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


urlpatterns = [
    path('administration/', admin.site.urls),

    # MODIFY: rest_api -> [앱이름]
    path('admin/', include('rest_api.urls.admin_urls')),
    path('auth/', include('rest_api.urls.auth_urls')),
    path('game/', include('rest_api.urls.game_urls')),
    path('lookup/', include('rest_api.urls.lookup_urls')),
]
