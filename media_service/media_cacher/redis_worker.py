import redis
import os


def start_redis_listener():
    r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
    pubsub = r.pubsub()
    pubsub.psubscribe("__keyevent@0__:expired")

    print("[RedisWorker] Слушаем Redis на истекшие ключи...")

    for message in pubsub.listen():
        if message["type"] == "pmessage":
            key = message["data"]
            if key.startswith("user_avatar_"):
                filename = key.replace("user_avatar_", "") + ".jpg"
                path = os.path.join("media_cache", filename)
                try:
                    os.remove(path)
                    print(f"[RedisWorker] Удалён: {path}")
                except FileNotFoundError:
                    print(f"[RedisWorker] Не найден: {path}")
