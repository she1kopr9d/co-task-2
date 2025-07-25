import django.contrib.auth.models

import rest_framework
import rest_framework.permissions
import rest_framework.decorators
import rest_framework.response
import rest_framework_simplejwt.views

import users.serializers
import users.kafka_producer


class CustomTokenObtainPairView(
    rest_framework_simplejwt.views.TokenObtainPairView,
):
    serializer_class = users.serializers.CustomTokenObtainPairSerializer


class CustomTokenRefreshView(rest_framework_simplejwt.views.TokenRefreshView):
    serializer_class = users.serializers.CustomTokenRefreshSerializer


class RegisterView(rest_framework.generics.CreateAPIView):
    queryset = django.contrib.auth.models.User.objects.all()
    serializer_class = users.serializers.RegisterSerializer
    permission_classes = [rest_framework.permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "registered_at": user.date_joined.isoformat(),
        }
        users.kafka_producer.send_user_registration_event(user_data)


@rest_framework.decorators.api_view(["GET"])
@rest_framework.decorators.permission_classes(
    [rest_framework.permissions.IsAuthenticated],
)
def user_info_view(request):
    user = request.user
    return rest_framework.response.Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    )
