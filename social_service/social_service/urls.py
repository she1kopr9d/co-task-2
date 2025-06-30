import django.contrib.admin
import django.urls


urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("profile/", django.urls.include("profile_app.urls")),
]
