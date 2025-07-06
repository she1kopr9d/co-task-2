import django.contrib.admin
import django.urls

import drf_spectacular.views

import media_cacher.views.avatar


urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path(
        "avatar/<int:user_id>/",
        media_cacher.views.avatar.UserAvatarAPIView.as_view(),
        name="avatar",
    ),
    django.urls.path(
        "avatar/upload/<int:user_id>/",
        media_cacher.views.avatar.AvatarUploadView.as_view(),
        name="upload-avatar",
    ),
    django.urls.path(
        "api/schema/",
        drf_spectacular.views.SpectacularAPIView.as_view(),
        name="schema",
    ),
    django.urls.path(
        "api/docs/",
        drf_spectacular.views.SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),
]
