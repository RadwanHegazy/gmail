from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Gmail Clone API",
        default_version='v1',
        description="API documentation for Gmail Clone project",
    ),
    public=True,
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('__docs__/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('users/', include('users.apis.urls')),
    path('mail/', include('mail.apis.urls')),
    path('spam/', include('spam.apis.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
