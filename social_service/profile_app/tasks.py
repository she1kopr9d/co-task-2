import celery


@celery.shared_task
def add(x, y):
    return x + y
