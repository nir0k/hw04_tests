from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..constants import POSTS_PER_PAGE

from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Ivank')
        cls.group = Group.objects.create(
            title='Test group 01',
            slug='test-group-01',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост для тестирования',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.author.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_fields = {
            first_object.text: self.post.text,
            first_object.group: self.post.group,
            first_object.author: self.post.author,
        }
        for field, expected in post_fields.items():
            with self.subTest(field=field):
                self.assertEqual(field, expected)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            )
        )
        first_object = response.context['page_obj'][0]
        post_fields = {
            first_object.text: self.post.text,
            first_object.author: self.post.author,
        }
        for field, expected in post_fields.items():
            with self.subTest(field=field):
                self.assertEqual(field, expected)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.author.username}
            )
        )
        first_object = response.context['page_obj'][0]
        post_fields = {
            first_object.text: self.post.text,
            first_object.author: self.post.author,
        }
        for field, expected in post_fields.items():
            with self.subTest(field=field):
                self.assertEqual(field, expected)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            )
        )
        self.assertEqual(response.context['post'].text, self.post.text)
        self.assertEqual(response.context['posts_count'], 1)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}
            )
        )
        self.assertEqual(response.context['is_edit'], True)
        self.assertEqual(response.context['post_id'], self.post.pk)
        self.assertEqual(
            response.context['form']['group'].initial,
            self.post.group.pk)
        self.assertEqual(
            response.context['form']['text'].initial,
            self.post.text)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        self.assertEqual(
            response.context['form']['group'].initial,
            None
        )
        self.assertEqual(
            response.context['form']['text'].initial,
            None
        )

    def test_paginator(self):
        """Тестирование работы пагинатора"""
        group_pagi = Group.objects.create(
            title='Test group 02',
            slug='test-02',
        )
        texts = ['This test text %d' % i for i in range(23)]
        for text in texts:
            Post.objects.create(
                text=text,
                author=self.author,
                group=group_pagi,
            )
        paginator_dict = {
            reverse('posts:index'): POSTS_PER_PAGE,
            reverse('posts:index') + '?page=3': 4,
            reverse(
                'posts:group_list',
                kwargs={'slug': group_pagi.slug}
            ): POSTS_PER_PAGE,
            reverse(
                'posts:group_list',
                kwargs={'slug': group_pagi.slug}
            ) + '?page=3': 3,
            reverse(
                'posts:profile',
                kwargs={'username': self.author.username}
            ): POSTS_PER_PAGE,
            reverse(
                'posts:profile',
                kwargs={'username': self.author.username}
            ) + '?page=3': 4,
        }
        for reverse_value, expected in paginator_dict.items():
            with self.subTest(reverse_value=reverse_value):
                response = self.client.get(reverse_value)                
                self.assertEqual(len(response.context['page_obj']), expected)
