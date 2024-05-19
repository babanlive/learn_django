from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Category, Husband, TagPost, Women


class GetPagesTestCase(TestCase):
    fixtures = [
        'women_women.json',
        'women_category.json',
        'women_husband.json',
        'women_tagpost.json',
    ]

    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertIn('women/index.html', response.template_name)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        post_list = Women.published.select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context_data['posts']), 5)
        self.assertQuerySetEqual(response.context_data['posts'], post_list[:5])

    def test_paginated_mainpage(self):
        path = reverse('home')
        page = 2
        paginate = 5
        response = self.client.get(path + f'?page={page}')
        post_lst = Women.published.select_related('cat')
        second_page_posts = post_lst[(paginate * (page - 1)) : (paginate * page)]
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context_data['posts']), 5)
        self.assertQuerySetEqual(response.context_data['posts'], second_page_posts)

    def test_show_post(self):
        post = Women.published.get(pk=3)
        path = reverse('post', kwargs={'post_slug': post.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['post'].content, post.content)

    def tearDown(self):
        "Действия после выполнения каждого теста"


class AddPageTestCase(TestCase):
    def setUp(self):
        """
        Инициализация перед выполнением каждого теста
        """
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='add_women'))

        Category.objects.create(name='Test Category', slug='test-category')
        TagPost.objects.create(tag='Test Tag', slug='test-tag')
        Husband.objects.create(name='Test Husband', age=20)

    def test_add_page_access_for_authenticated_user(self):
        """
        Проверка доступности страницы добавления статьи для авторизованного пользователя
        """
        self.client.force_login(self.user)
        path = reverse('add_page')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'women/addpage.html')
        self.assertEqual(response.context['title'], 'Добавление статьи')

    # def test_add_page_form_submission(self): # TODO
    #     """
    #     Проверка корректного создания новой статьи после заполнения формы
    #     """
    #     self.client.force_login(self.user)
    #     path = reverse('add_page')
    #     form_data = {
    #         'title': 'Test Title',
    #         'slug': 'test-title',
    #         'content': 'Test Content',
    #         'is_published': True,
    #         'cat': 2,
    #     }

    #     response = self.client.post(path, form_data)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.assertTrue(Women.objects.filter(title='Test Title').exists())
    #     new_post = Women.objects.get(title='Test Title')
    #     self.assertEqual(new_post.content, 'Test Content')

    def test_add_page_redirect_for_unauthenticated_user(self):
        """
        Проверка перенаправления на страницу входа для неавторизованного пользователя при попытке доступа к странице добавления статьи
        """
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def tearDown(self):
        """
        Действия после выполнения каждого теста
        """
        pass
