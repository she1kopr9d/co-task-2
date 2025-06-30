import django.urls
import django.conf.urls.i18n
import django.conf.urls.static
import django.contrib.admin

import frontend_service.settings


urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("auth/", django.urls.include("auth_ui.urls")),
]

urlpatterns += [
    django.urls.path("i18n/", django.urls.include("django.conf.urls.i18n")),
]

urlpatterns += django.conf.urls.i18n.i18n_patterns(
    django.urls.path("", django.urls.include("social_media.urls")),
    django.urls.path("", django.urls.include("guest.urls")),
    prefix_default_language=True,
)

if frontend_service.settings.DEBUG:
    urlpatterns += django.conf.urls.static.static(
        frontend_service.settings.MEDIA_URL,
        document_root=frontend_service.settings.MEDIA_ROOT,
    )
    urlpatterns += django.conf.urls.static.static(
        frontend_service.settings.STATIC_URL,
        document_root=frontend_service.settings.STATIC_ROOT,
    )
