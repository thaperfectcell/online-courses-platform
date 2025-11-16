from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('test-celery/', views.trigger_test_task, name='test_celery'),
    path("<int:pk>/enroll/", views.enroll_in_course, name="enroll"),

]
