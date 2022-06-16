from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from back_office.views import Menu

# A list of url patterns that are not translated.
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# A list of url patterns that are translated.
urlpatterns += i18n_patterns(
    path('', Menu, name='menu'),
    path('admin/', admin.site.urls),
    path('back_office/', include('back_office.urls')),
    path('', include('Users.urls')),
    path('api/', include('rest_api.urls')),
)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
