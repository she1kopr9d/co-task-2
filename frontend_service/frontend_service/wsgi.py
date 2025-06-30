import os

import django.core.wsgi


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend_service.settings")

application = django.core.wsgi.get_wsgi_application()
