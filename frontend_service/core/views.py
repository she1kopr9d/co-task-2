import django.http


def index(request):
    return django.http.HttpResponse("<h1>Hello from Co-Task Frontend!</h1>")
