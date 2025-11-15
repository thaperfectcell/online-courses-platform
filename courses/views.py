from django.shortcuts import render, get_object_or_404
from .models import Course
from django.http import HttpResponse
from .tasks import test_celery_task



def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
    })

def trigger_test_task(request):
    # Отправляем задачу в Celery
    test_celery_task.delay()
    return HttpResponse("Задача Celery отправлена в очередь")
