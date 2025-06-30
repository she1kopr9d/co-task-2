import threading

import django.apps


class MediaCacherConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "media_cacher"

    def ready(self):
        import media_cacher.redis_worker

        threading.Thread(
            target=media_cacher.redis_worker.start_redis_listener,
            daemon=True,
        ).start()
