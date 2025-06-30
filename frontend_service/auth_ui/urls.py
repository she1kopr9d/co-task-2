import django.urls

import auth_ui.views


app_name = "auth_ui"

urlpatterns = [
    django.urls.path(
        "register/", auth_ui.views.register_view, name="register"
    ),
    django.urls.path("login/", auth_ui.views.login_view, name="login"),
]
