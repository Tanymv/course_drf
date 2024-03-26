from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(id=1, email='user@test.ru', password='12345', is_active=True)
        self.client.force_authenticate(user=self.user)

        """Создание тестовой полезной привычки"""
        self.habit = Habit.objects.create(
            user=self.user,
            action='Тестовая полезная привычка_1',
            place='В случайном месте',
            duration='20'
        )

    def test_user_habit_list(self):
        """Тестирование списка привычек для авторизованного пользователя"""
        response = self.client.get(reverse('habits:my_habit_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_published_habit_list(self):
        """Тестирование списка опубликованых привычек"""
        Habit.objects.create(
            user=self.user,
            action='Тестовая полезная привычка_2',
            place='В случайном месте',
            duration='20',
            is_published=True
        )

        response = self.client.get(reverse('habits:habit_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        data = {'duration': 10,
                'action': 'Тестовая полезная привычка_2', 'place': 'В случайном месте',
                'user': self.user.id}
        response = self.client.post('/habits/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.filter(action=data['action']).exists())

    def test_retrieve_habit(self):
        """Тестирование просмотра привычки"""
        path = reverse('habits:habit_view', [self.habit.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], self.habit.action)

    def test_update_habit(self):
        """Тестирование редактирования привычки"""
        path = reverse('habits:habit_update', [self.habit.id])
        data = {'duration': '15', 'reward': 'Отдохнуть'}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.reward, data['reward'])

    def test_delete_lesson_permission(self):
        """Проверка на права доступа: создан пользователь - не владелец привычки"""
        user_2 = User.objects.create(id=2, email='user_2@test.ru',
                                     password='12345')
        self.client.force_authenticate(user=user_2)

        path = reverse('habits:habit_delete', [self.habit.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson(self):
        """Тестирование удаления привычки"""
        self.client.force_authenticate(user=self.user)
        path = reverse('habits:habit_delete', [self.habit.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())