import django.http

import rest_framework.status
import rest_framework.views
import rest_framework.permissions
import rest_framework.parsers
import rest_framework.response

import logic.avatar


class UserAvatarAPIView(rest_framework.views.APIView):
    def get(self, request, user_id):
        path = logic.avatar.get_cached_avatar(user_id)

        if not path:
            path = logic.avatar.download_and_cache_avatar(user_id)
            if not path:
                return rest_framework.response.Response(
                    {
                        "error": "Not found in S3",
                    },
                    status=rest_framework.status.HTTP_404_NOT_FOUND,
                )

        return django.http.FileResponse(
            open(path, "rb"), content_type="image/jpeg"
        )


class AvatarUploadView(rest_framework.views.APIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    parser_classes = [rest_framework.parsers.MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return rest_framework.response.Response(
                {"detail": "No file uploaded"},
                status=rest_framework.status.HTTP_400_BAD_REQUEST,
            )

        user_id = request.user.id
        manager = logic.avatar.AvatarManager(user_id)

        try:
            s3_key = manager.resize_and_upload(file, size=(300, 300))
        except Exception as e:
            return rest_framework.response.Response(
                {"detail": str(e)},
                status=rest_framework.status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return rest_framework.response.Response(
            {"detail": "Avatar uploaded", "s3_key": s3_key}
        )
