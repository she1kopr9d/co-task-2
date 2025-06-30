import django.contrib.admin
import django.urls

import media_cacher.views.avatar


urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path(
        "avatar/<int:user_id>/",
        media_cacher.views.avatar.UserAvatarAPIView.as_view(),
        name="avatar",
    ),
    django.urls.path(
        "upload/avatar/<int:user_id>/",
        media_cacher.views.avatar.AvatarUploadView.as_view(),
        name="upload-avatar",
    ),
]
