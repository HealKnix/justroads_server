"""
URL configuration for justroads_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path,
    include,
)
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularAPIView,
    SpectacularRedocView,
)

from justroads.views import (
    AuthenticatedAPIView,
    LoginViewSet,
    LogoutViewSet,
)

urlpatterns = [
    path(
        '',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path('admin/', admin.site.urls),
    path('auth-login/', AuthenticatedAPIView.as_view(), name='auth-login'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('logout/', LogoutViewSet.as_view(), name='logout'),
    path('api/v1/', include('justroads.urls'), name='api'),
    # path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

    # Yaml openapi
    path('api/openapi/', SpectacularAPIView.as_view(), name='schema'),

    # Optional UI:
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
