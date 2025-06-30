import rest_framework.views
import rest_framework.response
import rest_framework.status
import rest_framework.permissions

import profile_app.models
import profile_app.serializers

import shared.settings


class CreateProfileView(rest_framework.views.APIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]

    def post(self, request):
        print(f"[CreateProfileView] - user_id {request.user_id}")
        user_id = request.user_id

        if profile_app.models.Profile.objects.filter(user_id=user_id).exists():
            print("[CreateProfileView] Profile is exist")
            return rest_framework.response.Response(
                {"detail": "Profile already exists."},
                status=rest_framework.status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["user_id"] = user_id
        data["avatar_url"] = (
            f"{shared.settings.MEDIA_SERVICE_URL}/avatar/{user_id}"
        )

        serializer = profile_app.serializers.ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return rest_framework.response.Response(
                serializer.data,
                status=rest_framework.status.HTTP_201_CREATED,
            )
        else:
            print(
                f"[CreateProfileView] Serializer errors: {serializer.errors}"
            )
            return rest_framework.response.Response(
                serializer.errors,
                status=rest_framework.status.HTTP_400_BAD_REQUEST,
            )


class GetMyProfileView(rest_framework.views.APIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user_id

        try:
            profile = profile_app.models.Profile.objects.get(user_id=user_id)
            serializer = profile_app.serializers.ProfileSerializer(profile)
            return rest_framework.response.Response(serializer.data)
        except profile_app.models.Profile.DoesNotExist:
            return rest_framework.response.Response(
                {"detail": "Profile not found."},
                status=rest_framework.status.HTTP_404_NOT_FOUND,
            )
