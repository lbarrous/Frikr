"""frikr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from photos.api import PhotoViewSet
from rest_framework.routers import DefaultRouter
from users.api import UserViewSet
from users import urls as users_urls, api_urls as users_api_urls
from photos import urls as photos_urls, api_urls as photos_api_urls


# APIRouters

router = DefaultRouter()
router.register(r'api/1.0/photos', PhotoViewSet)
router.register(r'api/1.0/users', UserViewSet, base_name='user')

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # User URLS
    url(r'', include(users_urls)),
    url(r'api/', include(users_api_urls)),

    # Photos URLS
    url(r'', include(photos_urls)),
    url(r'api/', include(photos_api_urls)),
]
