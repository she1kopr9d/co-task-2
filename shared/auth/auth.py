import os
import requests
import functools

import django.http

import rest_framework
import rest_framework.authentication
import rest_framework.exceptions
import rest_framework.status

import shared.settings
import shared.auth.jwt


def extract_request(args):
    for arg in args:
        if isinstance(arg, django.http.HttpRequest):
            return arg
    raise ValueError("Request not found in arguments")


def require_auth(view_func):
    @functools.wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = extract_request(args)
        secret_key = os.environ.get("DJANGO_SECRET_KEY", "some-default")
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return django.http.JsonResponse(
                {"detail": "Authorization credentials were not provided."},
                status=rest_framework.status.HTTP_401_UNAUTHORIZED,
            )

        try:
            data = shared.auth.jwt.decode_jwt(access_token, secret_key)
            return view_func(
                *args,
                jwt_token=data,
                **kwargs,
            )
        except Exception as error:
            if refresh_token:
                try:
                    response = requests.post(
                        f"{shared.settings.AUTH_SERVICE_URL}user/token/refresh/",
                        json={"refresh": refresh_token},
                        timeout=3,
                    )
                    if response.status_code == 200:
                        new_access = response.json().get("access")
                        data = shared.auth.jwt.decode_jwt(
                            new_access, secret_key
                        )
                        # Выполняем запрос один раз
                        response_view = view_func(
                            *args,
                            jwt_token=data,
                            **kwargs,
                        )

                        # Устанавливаем куку, если возможно
                        if hasattr(response_view, "set_cookie"):
                            response_view.set_cookie(
                                "access_token", new_access, httponly=True
                            )

                        return response_view
                except Exception as e:
                    pass  # Можно логировать здесь

            return django.http.JsonResponse(
                {"detail": "Invalid or expired token"},
                status=rest_framework.status.HTTP_401_UNAUTHORIZED,
            )

    return _wrapped_view


def check_jwt(request):
    token = request.COOKIES.get("access_token")

    if not token:
        request.jwt_data = None
        return request

    try:
        data = shared.auth.jwt.decode_jwt(
            token, os.environ.get("DJANGO_SECRET_KEY", "some-default")
        )
        request.jwt_data = {
            "user_id": data.get("user_id"),
            "username": data.get("username"),
            "email": data.get("email"),
            "is_staff": data.get("is_staff"),
        }
        return request
    except Exception:
        request.jwt_data = None
        return request


def get_user_from_request(request):
    token = request.COOKIES.get("access_token")
    if not token:
        auth_header = rest_framework.authentication.get_authorization_header(
            request
        ).decode("utf-8")
        if auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]

    if not token:
        raise rest_framework.exceptions.AuthenticationFailed(
            "Token not provided",
        )

    try:
        response = requests.get(
            f"{shared.settings.AUTH_SERVICE_URL}user/info/",
            headers={"Authorization": f"Bearer {token}"},
        )
    except requests.exceptions.RequestException:
        raise rest_framework.exceptions.AuthenticationFailed(
            "Auth service unavailable",
        )

    if response.status_code != 200:
        raise rest_framework.exceptions.AuthenticationFailed("Invalid token")

    return response.json()
