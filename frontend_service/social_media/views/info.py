import django.shortcuts

import rest_framework.decorators
import rest_framework.response
import rest_framework.renderers


@rest_framework.decorators.api_view(["GET"])
@rest_framework.decorators.renderer_classes(
    [rest_framework.renderers.TemplateHTMLRenderer],
)
def feed_view(request):
    if not request.user_id:
        return django.shortcuts.redirect("auth_ui:login")
    context = {"username": request.jwt_payload["username"]}
    return rest_framework.response.Response(
        context, template_name="social_media/feed.html"
    )
