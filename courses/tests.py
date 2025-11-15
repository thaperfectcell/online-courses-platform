from django.test import TestCase, Client
from django.urls import reverse

from .models import Course


class CoursesViewsTests(TestCase):
    def setUp(self):
        # Перед каждым тестом создаём один курс в тестовой БД
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса"
        )
        self.client = Client()

    def test_courses_list_page_returns_200(self):
        """
        Страница списка курсов /courses/ должна открываться (HTTP 200).
        """
        url = reverse("courses:course_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_course_detail_page_returns_200(self):
        """
        Страница конкретного курса /courses/<id>/ тоже должна открываться.
        """
        url = reverse("courses:course_detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
