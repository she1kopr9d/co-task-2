import rest_framework
import rest_framework.serializers

import profile_app.models


class ProfileSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = profile_app.models.Profile
        fields = [
            "id",
            "user_id",
            "bio",
            "avatar_url",
            "location",
            "birthdate",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "avatar_url",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user_id"):
            validated_data["user_id"] = request.user_id
        else:
            raise rest_framework.serializers.ValidationError(
                "User ID is missing in request."
            )

        return super().create(validated_data)
