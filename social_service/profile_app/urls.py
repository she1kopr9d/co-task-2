import django.urls

import profile_app.views


urlpatterns = [
    django.urls.path(
        "",
        profile_app.views.GetMyProfileView.as_view(),
        name="my_profile",
    ),
    django.urls.path(
        "create/",
        profile_app.views.CreateProfileView.as_view(),
        name="create_profile",
    ),
]
