import os

import django.core.asgi


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend_service.settings")

application = django.core.asgi.get_asgi_application()
