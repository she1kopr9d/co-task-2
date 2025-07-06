import django.contrib.admin
import django.urls

import drf_spectacular.views


urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("profile/", django.urls.include("profile_app.urls")),
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
