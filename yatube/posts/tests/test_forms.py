from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Post, Group
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Ivank')
        cls.group = Group.objects.create(
            title='Test group 01',
            slug='test-group-01',
        )
        cls.post_text = 'Тестовый пост'
        cls.post_to_edit = Post.objects.create(
            text=cls.post_text,
            author=cls.author,
            group=cls.group,
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': self.post_text,
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={'username': self.author.username}
            )
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.author,
                text=self.post_text,
                group=self.group,
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма редактирования записи в Post."""
        form_data = {
            'text': self.post_text + ' 01',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post_to_edit.pk}
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post_to_edit.pk}
            )
        )
        self.assertTrue(
            Post.objects.filter(
                author=self.author,
                text=self.post_text + ' 01',
                group=self.group.pk,
            ).exists()
        )
