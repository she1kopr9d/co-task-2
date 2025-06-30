import django.contrib.auth.models

import rest_framework
import rest_framework.serializers
import rest_framework_simplejwt.serializers
import rest_framework_simplejwt.tokens
import rest_framework_simplejwt.exceptions


class CustomTokenObtainPairSerializer(
    rest_framework_simplejwt.serializers.TokenObtainPairSerializer,
):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["is_staff"] = user.is_staff or user.is_superuser

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user_id"] = self.user.pk
        data["username"] = self.user.username
        data["is_staff"] = self.user.is_staff or self.user.is_superuser

        return data


class CustomTokenRefreshSerializer(
    rest_framework_simplejwt.serializers.TokenRefreshSerializer,
):
    def validate(self, attrs):
        data = super().validate(attrs)
        access = rest_framework_simplejwt.tokens.AccessToken(
            token=data["access"],
        )
        try:
            user = django.contrib.auth.models.User.objects.get(
                id=access["user_id"],
            )
            access["username"] = user.username
            access["is_staff"] = user.is_staff or user.is_superuser
        except django.contrib.auth.models.User.DoesNotExist:
            raise rest_framework_simplejwt.exceptions.InvalidToken(
                "User does not exist",
            )

        data["access"] = str(access)
        return data


class RegisterSerializer(rest_framework.serializers.ModelSerializer):
    password = rest_framework.serializers.CharField(write_only=True)

    class Meta:
        model = django.contrib.auth.models.User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = django.contrib.auth.models.User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user
