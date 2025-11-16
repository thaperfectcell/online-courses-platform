from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required   
from .models import Course, Enrollment
from django.http import HttpResponse
from .tasks import test_celery_task, send_enrollment_notification
from django.core.cache import cache



def course_list(request):
    # Пытаемся взять список курсов из кэша
    courses = cache.get("courses_list")

    if courses is None:
        # Если в кэше нет — читаем из БД
        courses = list(Course.objects.all())
        # Кладём в кэш на 60 секунд (можно больше, например 300)
        cache.set("courses_list", courses, 60)

    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, pk):
    cache_key = f"course_detail_{pk}"
    data = cache.get(cache_key)

    if data is None:
        course = get_object_or_404(Course, pk=pk)
        lessons = list(course.lessons.all())
        is_enrolled = False
        if request.user.is_authenticated:
            is_enrolled = Enrollment.objects.filter(
                user=request.user,
                course=course,
            ).exists()

        data = {
            "course": course,
            "lessons": lessons,
            "is_enrolled": is_enrolled,
        }
        cache.set(cache_key, data, 60)
    else:
        course = data["course"]
        lessons = data["lessons"]
        is_enrolled = data["is_enrolled"]

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
    })

def trigger_test_task(request):
    # Отправляем задачу в Celery
    test_celery_task.delay()
    return HttpResponse("Задача Celery отправлена в очередь")

@login_required
def enroll_in_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
    )

    if created:
        # Если запись на курс создана впервые — запускаем Celery-задачу
        send_enrollment_notification.delay(request.user.id, course.id)

    # Всегда возвращаем пользователя на страницу курса
    return redirect('courses:course_detail', pk=course.id)

