from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from course.models import Course, Lesson, Subscription

User = get_user_model()

class CourseTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user21@1.ru')
        self.course = Course.objects.create(name='Test Course', owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', course=self.course)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse('course:lesson-create')
        data = {'name': 'New Lesson', 'course': self.course.pk, 'video': 'https://www.youtube.com/watch?v=2g811Eo7K8U'}
        response = self.client.post(url, data, format='json')
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_retrieve_lesson(self):
        url = reverse('course:lesson-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)


    def test_update_lesson(self):
        url = reverse('course:lesson-update', args=[self.lesson.pk])
        data = {'name': 'Updated Lesson'}
        response = self.client.patch(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Updated Lesson')

    def test_delete_lesson(self):
        url = reverse('course:lesson-delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.pk).exists())


    def test_subscription(self):
        url = reverse('course:subscribe')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
