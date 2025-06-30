import os
import io
import PIL
import redis

import logic.storage


redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

CACHE_DIR = "media_cache"
REDIS_TTL = 3600


def get_avatar_filename(user_id: int) -> str:
    return f"avatar/user_{user_id}.jpg"


def get_avatar_local_path(user_id: int) -> str:
    return os.path.join(CACHE_DIR, get_avatar_filename(user_id))


def get_avatar_redis_key(user_id: int) -> str:
    return f"avatar/user_avatar_{user_id}"


def get_cached_avatar(user_id: int) -> str | None:
    redis_key = get_avatar_redis_key(user_id)
    path = redis_client.get(redis_key)

    if path:
        path = path.decode()
        if os.path.exists(path):
            return path
    return None


def download_and_cache_avatar(user_id: int) -> str | None:
    local_path = get_avatar_local_path(user_id)
    s3_key = get_avatar_filename(user_id)
    redis_key = get_avatar_redis_key(user_id)

    if logic.storage.download_file_from_s3(s3_key, local_path):
        redis_client.setex(redis_key, REDIS_TTL, local_path)
        return local_path
    return None


class AvatarManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.s3_prefix = f"avatars/{self.user_id}/"

    def resize_and_upload(self, file, size=(300, 300)):
        image = PIL.Image.open(file).convert("RGB")

        # Режем и масштабируем под точный размер
        image = PIL.ImageOps.fit(
            image, size, PIL.Image.ANTIALIAS, centering=(0.5, 0.5)
        )
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        key = f"{self.s3_prefix}avatar_{size[0]}x{size[1]}.jpg"
        logic.storage.upload_to_s3(key, buffer)
        return key
