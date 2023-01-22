import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, override_settings, TransactionTestCase
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache


from posts.models import Post, Group, Comment

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TransactionTestCase):
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
        cls.comment = Comment.objects.create(
            text='Тестовый комент для тестирования',
            author=cls.author,
            post=cls.post,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_index_page_cache(self):
        cache.clear()
        self.guest_client.get(reverse('posts:index'))
        with self.assertNumQueries(0):
            self.guest_client.get(reverse('posts:index'))
