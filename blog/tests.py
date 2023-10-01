from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@emai@.com',
            password='secret',
        )
        self.post = Post.objects.create(
            title='elmemo',
            body='oshi',
            author=self.user,
        )

    
    def test_string_representation(self):
        post = Post(title='A simple title')
        self.assertEqual(str(post),post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'elmemo')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'oshi')
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'oshi')
        self.assertTemplateUsed(response,'home.html')
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response,'elmemo')
        self.assertTemplateUsed(response,'post_detail.html')
