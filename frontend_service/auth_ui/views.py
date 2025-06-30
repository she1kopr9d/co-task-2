import requests

import django.shortcuts

import shared.settings


def register_view(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "password2": request.POST.get("password2"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
        }

        try:
            response = requests.post(
                f"{shared.settings.AUTH_SERVICE_URL}user/register/",
                data=data,
            )
        except requests.exceptions.RequestException:
            return django.shortcuts.render(
                request,
                "auth_ui/register.html",
                {"error": {"error": "Сервис авторизации временно недоступен"}},
            )

        if response.status_code == 201:
            return django.shortcuts.redirect("auth_ui:login")

        try:
            error_data = response.json()
        except ValueError:
            error_data = {"error": "Ошибка регистрации. Попробуйте позже."}

        return django.shortcuts.render(
            request,
            "auth_ui/register.html",
            {
                "error": error_data,
            },
        )

    return django.shortcuts.render(request, "auth_ui/register.html")


def login_view(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        try:
            response = requests.post(
                f"{shared.settings.AUTH_SERVICE_URL}user/token/",
                data=data,
            )
        except requests.exceptions.RequestException:
            return django.shortcuts.render(
                request,
                "auth_ui/login.html",
                {
                    "error": "Ошибка связи с сервисом "
                    "авторизации. Попробуйте позже."
                },
            )

        if response.status_code == 200:
            access_token = response.json().get("access")
            refresh_token = response.json().get("refresh")
            resp = django.shortcuts.redirect("/feed/")
            resp.set_cookie("access", access_token, httponly=True)
            resp.set_cookie("refresh", refresh_token, httponly=True)
            return resp

        return django.shortcuts.render(
            request,
            "auth_ui/login.html",
            {"error": "Неверное имя пользователя или пароль"},
        )

    return django.shortcuts.render(request, "auth_ui/login.html")
