from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post

from rest_framework.test import APIClient


User = get_user_model()


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_a', password='somepassword')

    def test_post_created(self):
        post_obj = Post.objects.create(content='my post', user=self.user)
        self.assertEqual(post_obj.id, 1)
        self.assertEqual(post_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_post_list(self):
        client = self.get_client()
        response = client.get('api/posts/')
        self.assertEqual(response.status_code, 404)
        print(response.json())