from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class GetPagesTestCase(TestCase):
    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        print(dir(response))
        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertTemplateUsed(response, 'women/index.html')

    def test_case_1(self):
        pass

    def test_case_2(self):
        pass

    def tearDown(self):
        "Действия после выполнения каждого теста"
 