import django.http
import django.shortcuts

import shared.auth.auth


def index(request: django.http.HttpRequest):
    request = shared.auth.auth.check_jwt(request)
    if request.user_id is not None:
        return django.shortcuts.redirect("feed")
    return django.shortcuts.render(request, "guest/main.html")
