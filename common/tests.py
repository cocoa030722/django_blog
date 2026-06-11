from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class CommonViewsTestCase(TestCase):
    def test_logout_view(self):
        response = self.client.get(reverse('common:logout'))
        self.assertEqual(response.status_code, 302)  # 로그아웃 시 302 리다이렉트 코드를 반환해야 함
    def test_signup_view(self):
        response = self.client.get(reverse('common:signup'))  # GET 요청 테스트
        self.assertEqual(response.status_code, 200)  # GET 요청 시 200 코드를 반환해야 함
        new_user_data = {'username': 'testuser',
                        'password1': 'testpassword123',
                         'password2': 'testpassword123',
                         'email': 'qwer@qwer.com'
                        }
        response = self.client.post(reverse('common:signup'), new_user_data)  # POST 요청 테스트

        self.assertEqual(response.status_code, 301)  # 회원가입 성공 시 301 영구 리다이렉트 코드를 반환해야 함
        new_user = User.objects.get(username='testuser')  # 새로운 사용자 객체를 가져옴
        self.assertIsNotNone(new_user)  # 새로운 사용자가 존재해야 함