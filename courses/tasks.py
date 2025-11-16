from celery import shared_task
import time
from django.contrib.auth import get_user_model
from .models import Course
from django.core.mail import send_mail

User = get_user_model()

@shared_task
def send_enrollment_notification(user_id: int, course_id: int) -> str:
    """
    Фоновая задача: отправить письмо пользователю о записи на курс.
    Выполняется через Celery + Redis, чтобы не блокировать основной запрос.
    """
    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
    except (User.DoesNotExist, Course.DoesNotExist):
        return "user_or_course_not_found"

    subject = f"Вы записались на курс: {course.title}"
    message = (
        f"Здравствуйте, {user.username}!\n\n"
        f"Вы успешно записались на курс «{course.title}».\n"
        f"Дата записи будет сохранена в вашем личном кабинете.\n\n"
        f"С уважением,\nПлатформа онлайн-курсов"
    )

    # Письмо уйдёт в тот backend, который настроен в settings.EMAIL_BACKEND
    if user.email:
        send_mail(
            subject,
            message,
            None,             # from_email → возьмётся из DEFAULT_FROM_EMAIL
            [user.email],
            fail_silently=True,
        )
    else:
        # Если у пользователя нет email — хотя бы залогируем
        print(f"[EMAIL] У пользователя {user.username} не задан email, письмо не отправлено")

    print(f"[CELERY] Обработана запись на курс: {user.username} → {course.title}")
    return "ok"

@shared_task
def test_celery_task():
    print("Запускаю тестовую задачу Celery...")
    time.sleep(5)
    print("Тестовая задача Celery завершена")
    return "ok"
