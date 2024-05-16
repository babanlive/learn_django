from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Women


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
