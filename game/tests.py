from django.test import TestCase
from .models import MainUser, SubUser
from django.contrib.auth.models import User
from django.urls import reverse
from unittest import mock
# Create your tests here.

class MyModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.main_user = MainUser.objects.create(owner=self.user, choice='rock')
        self.sub_user = SubUser.objects.create(owner=self.user, main_user=self.main_user, choice='scissors')

    def test_main_user_creation(self):
        self.assertEqual(self.main_user.owner.username, 'testuser')
        self.assertEqual(self.main_user.choice, 'rock')

    def test_sub_user_creation(self):
        self.assertEqual(self.sub_user.owner.username, 'testuser')
        self.assertEqual(self.sub_user.main_user, self.main_user)
        self.assertEqual(self.sub_user.choice, 'scissors')
        
class GameTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_index_view(self):
        response = self.client.get(reverse('game:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/index.html')

    def test_create_game_view(self):
        response = self.client.post(reverse('game:create_game'), {'choice': 'rock'})
        self.assertEqual(response.status_code, 302)  # Check if it redirects upon successful POST request
        main_user = MainUser.objects.first()
        self.assertEqual(main_user.owner, self.test_user)
        self.assertEqual(main_user.choice, 'rock')

    def test_sub_user_choice_view(self):
        main_user = MainUser.objects.create(owner=self.test_user, choice='scissors')
        response = self.client.get(reverse('game:sub_user_choice', kwargs={'main_pk': main_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/sub_user_choice.html')
        self.assertEqual(response.context['main_pk'], main_user.pk)

class SendChoiceTestCase(TestCase):

    def test_send_choice_with_post_request(self):
        main_user = MainUser.objects.create(choice='rock')
        data = {
            'mainPk': main_user.pk,
            'subChoice': 'scissors'
        }
        response = self.client.post(reverse('game:send_choice'), data, content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertTrue('gameResult' in response.json())
        self.assertTrue('mainUserChoice' in response.json())
        self.assertTrue('subUserChoice' in response.json())
    
    def test_get_main_with_post_request(self):
        main_user = MainUser.objects.create(choice='rock')
        data = {
            'mainPk': main_user.pk,
        }
        response = self.client.post(reverse('game:get_main'), data, content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertTrue('mainUserChoice' in response.json())
    
    @mock.patch('django.http.HttpResponse')
    def test_socket_test(self, mock_render):
        response = self.client.get(reverse('game:socket_test'))
    
        self.assertEqual(response.status_code, 200)
        mock_render.assert_called_with('game/socket_test.html')