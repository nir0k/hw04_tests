import tempfile
import shutil
import base64

from django.contrib.auth import get_user_model
from posts.forms import PostForm, CommentForm
from posts.models import Post, Group, Comment
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Ivank')
        cls.group = Group.objects.create(
            title='Test group 01',
            slug='test-group-01',
        )
        cls.post_text = 'Тестовый пост'
        cls.form = PostForm()
        cls.post_to_edit = Post.objects.create(
            text=cls.post_text,
            author=cls.author,
            group=cls.group,
        )
        cls.small_bmp = base64.b64decode(
            'Qk0eAAAAAAAAABoAAAAMAAAAAQABAAEAGAAAAP8A')
        cls.comment_form = CommentForm()
        cls.comment_text = 'Тестовый комментарий'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
        self.uploaded = SimpleUploadedFile(
            name='small.bmp',
            content=self.small_bmp,
            content_type='image/bmp'
        )

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': self.post_text,
            'group': self.group.pk,
            'image': self.uploaded,
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
                image=f'posts/{self.uploaded.name}',
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма редактирования записи в Post."""
        uploaded = SimpleUploadedFile(
            name='small1.bmp',
            content=self.small_bmp,
            content_type='image/bmp'
        )
        form_data = {
            'text': f'{self.post_text}01',
            'group': self.group.pk,
            'image': uploaded,
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
                text=f'{self.post_text}01',
                group=self.group.pk,
                image=f'posts/{uploaded.name}'
            ).exists()
        )

    def test_create_comment(self):
        """Валидная форма создает новый комментарий."""
        comments_count = Comment.objects.count()
        form_data = {
            'text': self.comment_text,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
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
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                author=self.author,
                text=self.comment_text,
                post=self.post_to_edit,
            ).exists()
        )
