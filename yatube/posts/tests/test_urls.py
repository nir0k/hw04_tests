from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from ..models import Post, Group

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Ivank')
        cls.group = Group.objects.create(
            title='Test group 01',
            slug='test-group-01',
        )

        cls.post = Post.objects.create(
            text='Тестовый пост для тестирования теста',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
        self.guest_pages = {
            '/': 200,
            f'/group/{self.group.slug}/': 200,
            f'/profile/{self.post.author}/': 200,
            f'/posts/{self.post.pk}/': 200,
            '/unexisting_page/': 404,
        }
        self.guest_page_templates = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.post.author}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }

    def test_home_url_exists_at_desired_location(self):
        """Тест общедоступных страниц"""
        for url, response_code in self.guest_pages.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, response_code)

    def test_create_url(self):
        """Страница /create/ доступна только авторизованным пользователям"""
        url = '/create/'
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.guest_client.get(url)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_create_url(self):
        """Страница /posts/<post_id>/edit/ доступна только автору"""
        url = f'/posts/{self.post.pk}/edit/'
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.guest_client.get(url, follow=True)
        self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_urls_used_templates(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.guest_page_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
