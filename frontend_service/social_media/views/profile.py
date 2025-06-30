import django.views
import django.shortcuts

import shared.settings
import shared.requests.frontend_request


class CreateProfileView(django.views.View):
    def get(self, request):
        return django.shortcuts.render(
            request, "social_media/profile_create.html"
        )

    def post(
        self,
        request,
    ):
        if not request.user_id:
            return django.shortcuts.redirect("login")

        bio = request.POST.get("bio", "")
        avatar_url = f"{shared.settings.MEDIA_SERVICE_URL}avatar/{
            request.user_id}/"

        payload = {
            "bio": bio,
            "avatar": avatar_url,
        }

        try:
            response = shared.requests.frontend_request.make_authenticated_service_request(
                request,
                method="POST",
                url=f"{shared.settings.SOCIAL_SERVICE_URL}" "profile/create/",
                json=payload,
            )
        except Exception:
            return django.shortcuts.render(
                request,
                "social_media/profile_create.html",
                {"error": "Ошибка соединения с сервером", "bio": bio},
            )

        if response.status_code == 201:
            return django.shortcuts.redirect("feed")
        else:
            error = response.json().get(
                "detail", "Ошибка при создании профиля"
            )
            return django.shortcuts.render(
                request,
                "social_media/profile_create.html",
                {"error": error, "bio": bio},
            )
