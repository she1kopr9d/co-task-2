import os
import celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_service.settings")

app = celery.Celery("social_service")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
