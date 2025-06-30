import requests
import django.utils.timezone

import rest_framework_simplejwt.tokens
import rest_framework_simplejwt.exceptions

import shared.settings


class JWTOptionalAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("[JWTMiddleware] Start call")
        print("[JWTMiddleware] Cookies:", request.COOKIES)
        print("[JWTMiddleware] Headers:", request.headers)

        request.jwt_payload = None
        request.user_id = None
        request.new_access_token = None
        request.is_authenticated = False
        request.is_staff = False

        # === 1. Попробовать достать access token из заголовка ===
        auth_header = request.headers.get("Authorization")
        access = None
        refresh = None

        if auth_header and auth_header.startswith("Bearer "):
            access = auth_header.split(" ")[1]
            print(
                "[JWTMiddleware] Found Authorization header with Bearer token"
            )
        else:
            # === 2. Падать обратно на куки, если заголовка нет ===
            access = request.COOKIES.get("access")
            refresh = request.COOKIES.get("refresh")
            if access:
                print("[JWTMiddleware] Found access token in cookies")

        # === 3. Проверка access токена ===
        if access:
            try:
                token = rest_framework_simplejwt.tokens.AccessToken(access)
                if token["exp"] < int(django.utils.timezone.now().timestamp()):
                    raise rest_framework_simplejwt.exceptions.TokenError(
                        "Access token expired"
                    )

                request.jwt_payload = token.payload
                request.user_id = token["user_id"]
                request.is_authenticated = True
                request.is_staff = token.get("is_staff", False)
                print("[JWTMiddleware] Access token is valid")
            except rest_framework_simplejwt.exceptions.TokenError as err:
                print(f"[JWTMiddleware] Access token error: {err}")

        # === 4. Рефреш токена — ТОЛЬКО ЕСЛИ используется куки ===
        if not request.user_id and refresh:
            print("[JWTMiddleware] Trying to refresh access token")
            try:
                response = requests.post(
                    url=f"{shared.settings.AUTH_SERVICE_URL}user/token/refresh/",
                    json={"refresh": refresh},
                    timeout=2,
                )
                print(
                    f"[JWTMiddleware] Refresh response status: {response.status_code}"
                )

                if response.status_code == 200 and "access" in response.json():
                    new_access = response.json()["access"]
                    request.new_access_token = new_access

                    token = rest_framework_simplejwt.tokens.AccessToken(
                        new_access
                    )
                    request.jwt_payload = token.payload
                    request.user_id = token["user_id"]
                    request.is_authenticated = True
                    request.is_staff = token.get("is_staff", False)
                    print(
                        "[JWTMiddleware] Access token successfully refreshed"
                    )
                else:
                    print(f"[JWTMiddleware] Refresh failed: {response.text}")
            except Exception as e:
                print(f"[JWTMiddleware] Exception during token refresh: {e}")

        if not request.user_id:
            print("[JWTMiddleware] No valid tokens available")

        # === 5. Сохраняем новый access токен только если был в cookie (т.е. frontend) ===
        response = self.get_response(request)
        if request.new_access_token:
            response.set_cookie(
                key="access",
                value=request.new_access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
                max_age=300,
            )
            print("[JWTMiddleware] New access token set in cookies")

        return response
