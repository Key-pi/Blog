import pytest_django
import pytest
from django.contrib.auth.models import User
from boards.utils import division
from .views import login
from django import urls

@pytest.mark.django_db
def test_login(client):
    tmp = urls.reverse('accounts:login')
    response = client.get(tmp)
    print(response.status_code)
    assert response.status_code == 200




























# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.urls import resolve, reverse
#
# from .forms import SignUpForm
# from .views import signup
#
# #
# class SignUpTest(TestCase):
#     def setUp(self):
#         url = reverse('signup')
#         self.response = self.client.get(url)
#     def test_signup_status_code(self):
#         url = reverse('accounts:signup/')
#         response = self.client.get(url)
#         self.assertEquals(response, 200)
#     def test_signup_resolves_signup_view(self):
#         view = resolve('/signup/')
#         self.assertEquals(view.func, signup)
#     def test_csrf(self):
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#     def test_contains_form(self):
#         form = self.response.context.get('form')
#         self.assertIsInstance(form, SignUpForm)
#     def test_form_inputs(self):
#         self.assertContains(self.response, '<input', 5)
#         self.assertContains(self.response, 'type="text"', 1)
#         self.assertContains(self.response, 'type="email"', 1)
#         self.assertContains(self.response, 'type="password"', 2)
# # class SuccessfulSignUpTests(TestCase):
#     def setUp(self):
#         url = reverse('accounts:signup')
#         data = {
#             'username': 'john',
#             'email': 'john@doe.com',
#             'password1': 'abcdef123456',
#             'password2': 'abcdef123456',
#         }
#         self.response = self.client.post(url, data)
#         self.home_url = reverse('boards:home')
#
#     def test_redirection(self):
#         self.assertRedirects(self.response, self.home_url)
#
#     def test_user_creation(self):
#         self.assertTrue(User.objects.exist())
#
#     def test_user_authentication(self):
#         response = self.client.get(self.home_url)
#         user = response.context.get('user')
#         self.assertTrue(user.is_authenticated)
#
#
# class InvalidSignUpTests(TestCase):
#     def setUp(self):
#         url = reverse('accounts:signup')
#         self.response = self.client.post(url, {})
#
#     def test_signup_status_code(self):
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_form_errors(self):
#         form = self.response.context.get('form')
#         self.assertTrue(form.errors)
#
#     def test_dont_create_user(self):
#         self.assertFalse(User.objects.exists())
