from celery import shared_task
import time


@shared_task
def test_celery_task():
    print("Запускаю тестовую задачу Celery...")
    time.sleep(5)
    print("Тестовая задача Celery завершена")
    return "ok"
