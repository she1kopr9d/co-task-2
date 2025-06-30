import django.urls

import users.views


urlpatterns = [
    django.urls.path(
        "register/",
        users.views.RegisterView.as_view(),
        name="register",
    ),
    django.urls.path(
        "token/",
        users.views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    django.urls.path(
        "token/refresh/",
        users.views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    django.urls.path("info/", users.views.user_info_view),
]
