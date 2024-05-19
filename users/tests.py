from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user_1',
            'email': 'user1@sitewomen.ru',
            'first_name': 'Sergey',
            'last_name': 'Balakirev',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_form_registration_get(self):
        """
        Тестирование GET-запроса для регистрации формы.
        """
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_success(self):
        """
        Проверка успешной регистрации пользователя.
        """
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))

    def test_user_registration_password_error(self):
        """
        Проверка регистрации пользователя с неверно введеным повтором пароля.
        """
        self.data['password2'] = '12345678A'
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают.')

    def test_user_registration_user_exists_error(self):
        """
        Проверка регистрации пользователя, когда пользователь с таким же именем уже существует.
        """
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')
