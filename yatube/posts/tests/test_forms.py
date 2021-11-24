import shutil
import tempfile
from django.contrib.auth import get_user_model

from ..models import Post, Group
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
            group=cls.group
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает пост."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': 1
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'HasNoName'}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=1
            ).exists()
        )

    def test_edit_post(self):
        """При отправке валидной формы пост редактируется."""
        post = Post.objects.create(
            author=self.user,
            text='Тестовый текст'
        )
        edit_form_data = {
            'text': 'Отредактированный текст',
            'group': 1
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '2'}),
            data=edit_form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:post_detail', kwargs={'post_id': '2'}))
        self.assertTrue(
            Post.objects.filter(
                text='Отредактированный текст',
                group=1
            ).exists()
        )
