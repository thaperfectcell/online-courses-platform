from celery import shared_task
import time
from django.contrib.auth import get_user_model
from .models import Course

User = get_user_model()

@shared_task
def send_enrollment_notification(user_id: int, course_id: int) -> str:
    """
    Фоновая задача: "отправить письмо" или просто залогировать факт записи.
    В реальном проекте тут был бы SMTP или внешний сервис.
    """
    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
    except (User.DoesNotExist, Course.DoesNotExist):
        return "user_or_course_not_found"

    # Здесь вместо настоящей отправки письма просто печатаем в лог воркера:
    print(f"[CELERY] Пользователь {user.username} записался на курс '{course.title}'")

    # Мог бы быть реальный код отправки email:
    # send_mail(...)
    return "ok"

@shared_task
def test_celery_task():
    print("Запускаю тестовую задачу Celery...")
    time.sleep(5)
    print("Тестовая задача Celery завершена")
    return "ok"
